import logging
import os
import io
import zipfile

from flask_restful import Resource
from flask import request, jsonify, Response, send_file
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.items_model import Item, ImagesForItem
from models.users_model import User

UPLOAD_FOLDER = "static/images/"
ALLOWED_EXTENSIONS = {"jpg", "png", "bmp", "jpeg"}


class Images(Resource):
    def get(self):
        # item_id = request.form['item_id']
        item_id = request.args['item_id']
        item = Item.find_by_id(item_id=str(item_id))
        if not item:
            logging.error(f"Товар с item_id:{item_id} не найден!")
            return {"msg": "Item for picture not found"}, 404
        images = item.get_images()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as z:
            for image in images:
                with open(os.path.join(UPLOAD_FOLDER, image.filename), 'rb') as f:
                    image_data = f.read()
                z.writestr(image.filename, image_data)
        buffer.seek(0)
        return Response(image_data, content_type='image/jpeg')

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        if user.isAdmin:
            item_id = request.values['item_id']
            item = Item.find_by_id(item_id=str(item_id))
            if not item:
                logging.error(f"Товар с item_id:{item_id} не найден!")
                return {"msg": "Item for picture not found"}, 404
            f = request.files['file']
            extension = {f.filename.split(".")[1]}
            if extension.issubset(ALLOWED_EXTENSIONS):
                filename = secure_filename(f.filename)
                f.save(UPLOAD_FOLDER + filename)
                image = (ImagesForItem(item_id=item_id, filename=filename))
                item.images.append(image)
                item.save_to_db()
                logging.info(f"Картинка к товару {item_id} добавлена")
                return {"msg": "Image has been loaded"}, 200
            logging.error(f"Расширение картинки не поддерживается")
            return {"msg": "Image's extension isn't allowed"}, 400
        logging.error(f"Пользователь с user_id:{user_id} использовал недоступную для него функцию!")
        return {'msg': "You need to be an admin"}, 403

