from user_fd.tasks import send_register_active_email
import time

print('start')
t1 = time.time()
send_register_active_email('924304012@qq.com', '懒得做', 'token')
t2 = time.time()
t = t2 - t1
print(t)
# except Exception:
#     print(Exception)