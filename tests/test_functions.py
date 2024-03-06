from NAMeCSaverCam import functions as cam

img = cam.testresized
# step1 = cam.process_image_circle(img)
# step2 = cam.get_circle_from_img(step1)
# cam.show_image(step2)

mask = cam.process_image_green(img)
step2 = cam.get_green_from_img_new(img, mask)
cam.show_image(step2)