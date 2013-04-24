import SimpleCV
import sys

display = SimpleCV.Display()
camera = SimpleCV.Camera()

def swap_faces(frame):
    faces = frame.findHaarFeatures('face.xml')
    if faces is None:
        return frame

    for i in range(0, len(faces) - 1, 2):
        face = faces[i]
        next_face = faces[(i + 1) % len(faces)]

        mask = face.crop().resize(w=next_face.width(),\
            h=next_face.height())
        next_mask = next_face.crop().resize(w=face.width(),\
            h=face.height())

        mask_skin = mask.getSkintoneMask(0)
        mask_skin = mask_skin.dilate(3)

        next_mask_skin = next_mask.getSkintoneMask(0)
        next_mask_skin = next_mask_skin.dilate(3)

        frame = frame.blit(mask, next_face.topLeftCorner(), mask=mask_skin)
        frame = frame.blit(next_mask, face.topLeftCorner(), mask=next_mask_skin)
    return frame


def main():
    from_camera = False
    frame = None

    if len(sys.argv) >= 2:
        frame = SimpleCV.Image(sys.argv[1])
        swap_faces(frame).save(display)
    else:
        from_camera = True
        print "No image given as input. Using camera."

    while display.isNotDone():
        if from_camera:
            frame = camera.getImage()
            swap_faces(frame).save(display)

if __name__ == '__main__':
    main()

