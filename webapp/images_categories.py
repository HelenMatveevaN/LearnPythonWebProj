from webapp.model import db, ImagesCategories

def save_images_categories(id_image, id_category, labelled, confidence, updated_at):
    imgcats_imgcats = ImagesCategories(id_image=id_image, id_category=id_category, labelled=labelled, confidence=confidence, updated_at=updated_at)
    db.session.add(imgcats_imgcats)
    db.session.commit()