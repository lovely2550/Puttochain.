# ต้องติดตั้ง firebase-admin ใน requirements.txt เพื่อใช้งานจริง

# import firebase_admin 
# from firebase_admin import credentials
# from firebase_admin import messaging

class FCMNotifier:
    """
    Handles notifications for Karma, Nibbana Progress, and AI Guidance.
    """
    
    def __init__(self):
        # ในโปรเจกต์จริง ต้องมีการเริ่มต้น Firebase Admin SDK
        # cred = credentials.Certificate("path/to/serviceAccountKey.json")
        # if not firebase_admin._apps:
        #     firebase_admin.initialize_app(cred)
        pass

    def send_karma_update(self, user_fcm_token: str, new_karma_score: int, change: int):
        """
        Sends a notification when a user's Karma score is updated.
        """
        title = "✨ Karma Update!"
        body = f"Karma ของคุณมีการเปลี่ยนแปลง {change:+d} คะแนน! คะแนนรวม: {new_karma_score}"
        
        # message = messaging.Message(
        #     notification=messaging.Notification(title=title, body=body),
        #     token=user_fcm_token,
        # )
        
        # response = messaging.send(message)
        # print(f"Successfully sent Karma message: {response}")
        
        print(f"[FCM MOCK] Sent to {user_fcm_token}: {title} - {body}")

    def send_ai_guidance(self, user_fcm_token: str, advice: str):
        """
        Sends guidance from AI Somdej Ong Pathom.
        """
        title = "🙏 คำแนะนำจาก Somdej Ong Pathom"
        
        # message = messaging.Message(
        #     notification=messaging.Notification(title=title, body=advice),
        #     token=user_fcm_token,
        # )
        # response = messaging.send(message)
        # print(f"Successfully sent AI Guidance message: {response}")
        
        print(f"[FCM MOCK] Sent to {user_fcm_token}: {title} - {advice}")

# สามารถเรียกใช้ใน main.py หลังจากที่ Karma ถูกอัปเดต
# from puttochain.notification import FCMNotifier
# notifier = FCMNotifier()
# notifier.send_karma_update("USER_TOKEN_123", karma_db[user_id], karma_change)
