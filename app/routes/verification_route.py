from sqlalchemy.orm import Session
from database.database_main import get_db
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from models.users_model import User
from middlewares.auth import AuthMiddleware
import cloudinary
from cloudinary.uploader import upload, destroy
import os
from datetime import datetime


router = APIRouter(
    prefix="/verifications",
    tags=["Verification"]
)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
    )

class ImageTooLargeError(Exception):
    pass

class InvalidFileExtensionError(Exception):
    pass


@router.post("/users", status_code=status.HTTP_200_OK)
async def verify_user(image: UploadFile =File(...), current_user=Depends(AuthMiddleware), db: Session=Depends(get_db)):
    
    allowed_extns = ["png", "jpeg", "jpg"]

    file_extn = image.filename.split(".")[-1].lower()
    if not file_extn in allowed_extns:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid file extention. Change file to supported type")

    if current_user.verification.value == "verified":
            raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User already verified!"
        )

    try:
        content = image.file.read()
        file_size = len(content)
        if file_size > 5000000:
            raise ImageTooLargeError()
        
        image.file.seek(0)
        result = upload(image.file)
        url = result["secure_url"]
        # public_id = result["public_id"]

        current_user.image = url
        current_user.verification = "pending" 

        db.add(current_user)
        db.commit()
        db.refresh(current_user)

        return {
            "message": "Upload successful",
            "id": current_user.id,
            "image_url": current_user.image,
            "status": current_user.verification
            }

    except InvalidFileExtensionError:
        return {
            "message": "File with invalid extension"
        }
    except ImageTooLargeError as e:
        return {
            "message": "File size must not be greater than 5MB"
        }

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"ERROR: Failed to upload image: {e}"
        )
