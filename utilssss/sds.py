from fdfs_client.client import Fdfs_client

client = Fdfs_client(r'./client.conf')
ret = client.upload_by_filename(r'C:\Users\语\Pictures\壁纸\游戏\995708.jpg')
print(ret.get('Remote file_id'))