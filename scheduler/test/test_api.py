import requests
import json
r = requests.get('http://127.0.0.1:8888/api/test')
print "proc list mode 0: \n%s" % r.json()


data =    workorder_info = {
        "workOrderId": "aaaaaaaaa",
        "workOrderNo": "20151112150857104803",
        "workOrderType": 1,
        "workOrderConfig": {
            "payPattern": ""
        },
        "accountType": 4,
        "masterOrderId": "6d4ebf1bcfba4a28a354edacca9ae3e4",
        "orderId": "4af3b5d306eb46a3bfc47d127e09acde",
        "innerOrderId": "14a72dc107854e8db73b1b7991fb437e",
        "accountId": "051682e703624f1185fccfab9ae1f123",
        "userId": "614c1f6670484127bb1478a1a1d145fa",
        "serviceTag": "VMS1",
        "resourceId": "3b22631e801c4860a4bb420ab6edbdd0",
        "resourceType": "VM",
        "cycleType": 3,
        "workOrderItems": [
            {
                "workOrderItemId": 'aaaaa',
                "workOrderItemNo": "a20151112150857115903",
                "workOrderId": "1b3adb663c6d4b758e5360f767ef35ee",
                "masterOrderId": "6d4ebf1bcfba4a28a354edacca9ae3e4",
                "orderId": "4af3b5d306eb46a3bfc47d127e09acde",
                "innerOrderId": "14a72dc107854e8db73b1b7991fb437e",
                "innerOrderItemId": "54e64ecc1fae49199aa1ebee49f94bcc",
                "salesEntryId": "17ed2e07cf8111e39c2b9a348d686bbe",
                "productId": "461bb2f4d9414769b2b62d21cf2a7add",
                "serviceTag": "VMS1",
                "resourceType": "VM",
                "workOrderItemConfig": {
                    "platformId": "1111",
                    "vmName": "TestMQMsg",
                    "cpuNum": 2,
                    "memSize": 3,
                    "imageType": 0,
		            "securityGroupId":"",
                    "networkCards":[],
                    "osType": 2,
                    "imageId": "14bda65f-8a68-4401-b768-2f8fbe74ff9a",
                    "rootPassword": "idealpassword",
                    "keyPairId": "",
                    "InjectionFileType": "",
                    "InjectionFileAddr": "",
                    "vmNumber":1
                },
                "master": "true",
                "masterResourceId": "3b22631e801c4860a4bb420ab6edbdd0",
                "resourceId": "076c75a8fcd34a0a8283490a4b40c6c9",
                "cycleType": 3,
                "orderItemId": "7012b1f682974d74828de0874405e3c7"
            },
            {
                "workOrderItemId": 'dda12312',
                "workOrderItemNo": "20151112150857115903",
                "workOrderId": "1b3adb663c6d4b758e5360f767ef35ee",
                "masterOrderId": "6d4ebf1bcfba4a28a354edacca9ae3e4",
                "orderId": "4af3b5d306eb46a3bfc47d127e09acde",
                "innerOrderId": "14a72dc107854e8db73b1b7991fb437e",
                "innerOrderItemId": "54e64ecc1fae49199aa1ebee49f94bcc",
                "salesEntryId": "17ed2e07cf8111e39c2b9a348d686bbe",
                "productId": "461bb2f4d9414769b2b62d21cf2a7add",
                "master": "false",
                "serviceTag": "VMS1",
                "resourceType": "EBS",
                "workOrderItemConfig": {
                    "platformId": 2,
                    "sysVolumeType": "SATA",
                    "sysVolumeSize": 40,
                    "dataVolumes": [
                        {"type": "SATA","size":20},
                        {"type": "SSD", "size":30}
                    ]
                },
                "masterResourceId": "3b22631e801c4860a4bb420ab6edbdd0",
                "resourceId": "076c75a8fcd34a0a8283490a4b40c6c9",
                "cycleType": 3,
                "orderItemId": "7012b1f682974d74828de0874405e3c7"
            },
            {
                "workOrderItemId": '1111',
                "workOrderItemNo": "20151112150857115903",
                "workOrderId": "1b3adb663c6d4b758e5360f767ef35ee",
                "masterOrderId": "6d4ebf1bcfba4a28a354edacca9ae3e4",
                "orderId": "4af3b5d306eb46a3bfc47d127e09acde",
                "innerOrderId": "14a72dc107854e8db73b1b7991fb437e",
                "innerOrderItemId": "54e64ecc1fae49199aa1ebee49f94bcc",
                "salesEntryId": "17ed2e07cf8111e39c2b9a348d686bbe",
                "productId": "461bb2f4d9414769b2b62d21cf2a7add",
                "master": "false",
                "serviceTag": "VMS1",
                "resourceType": "NETWORK",
                "workOrderItemConfig": {
                    "platformId": '555',
                    "networkId":"",
                    "existFloatingIP":"",
                    "newBandwidthValue":0
                },
                "masterResourceId": "3b22631e801c4860a4bb420ab6edbdd0",
                "resourceId": "076c75a8fcd34a0a8283490a4b40c6c9",
                "cycleType": 3,
                "orderItemId": "7012b1f682974d74828de0874405e3c7"
            }

        ]
    }
r = requests.post('http://127.0.0.1:8888/api/resource/status', \
data='data='+json.dumps(data))
print "response: %s" % r.json()
