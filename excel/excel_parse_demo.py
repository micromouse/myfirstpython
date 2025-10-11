from excel.egypt_oppo_sales_clearance_generator import EgytpoppoSalesclearanceGenerator

# 生成[销售清关CI&PL]文件
EgytpoppoSalesclearanceGenerator \
    .initial(r"D:\Shadowbot\埃及-自动化开票流程-更新") \
    .set_handle_progress(lambda message: print(message)) \
    .generate()

print("done")
