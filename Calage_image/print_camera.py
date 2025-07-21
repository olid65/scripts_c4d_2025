import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    print("position : ",op.GetAbsPos())
    print("rotation : ",op.GetAbsRot())
    
    print("camera[c4d.CAMERA_FOCUS] : ", op[c4d.RSCAMERAOBJECT_FOCAL_LENGTH])
    print("camera[c4d.CAMERAOBJECT_APERTURE] : ", op[c4d.CAMERAOBJECT_APERTURE])

if __name__ == '__main__':
    main()