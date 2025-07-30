from utils import load_saved_model, prepare_image, predict_image

model, class_names = load_saved_model()


#image_array = prepare_image("C:\\Users\\Ali İhsan Sancar\\Desktop\\leukemia-classifier\\test_split_leukemia\\Benign\\WBC-Benign-002.jpg")
#image_array = prepare_image("C:\\Users\\Ali İhsan Sancar\\Desktop\\leukemia-classifier\\test_split_leukemia\\Early\\WBC-Malignant-Early-001.jpg")
#image_array = prepare_image("C:\\Users\\Ali İhsan Sancar\\Desktop\\leukemia-classifier\\test_split_leukemia\\Pre\WBC-Malignant-Pre-005.jpg")
image_array = prepare_image("C:\\Users\\Ali İhsan Sancar\\Desktop\\leukemia-classifier\\test_split_leukemia\\Pro\WBC-Malignant-Pro-006.jpg")


label = predict_image(image_array, model, class_names)

print("Tahmin:", label)