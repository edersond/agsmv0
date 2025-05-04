import os
from dotenv import load_dotenv ; load_dotenv('.env')
from supabase import create_client, Client
import jwt
from jose.exceptions import JWTError


supabase: Client = create_client(os.getenv('SPBURL'), os.getenv('SPBKEY'))
def verify_jwt(token: str) -> dict:
    """
    """
    try:
        payload = jwt.decode(token, os.getenv('SPBSECRET'), algorithms=[os.getenv('SPBALGO')], audience="authenticated")
        return payload
    except JWTError as e:
        print(f"JWT Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

