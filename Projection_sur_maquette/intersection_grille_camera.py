import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    cam = op
    
    if cam.CheckType(c4d.Ocamera):
        print('std')
        fov_h = cam[c4d.CAMERAOBJECT_FOV]
        fov_v = cam[c4d.CAMERAOBJECT_FOV_VERTICAL]
        
        offset_x = cam[c4d.CAMERAOBJECT_FILM_OFFSET_X]
        offset_y = cam[c4d.CAMERAOBJECT_FILM_OFFSET_Y]
        
        focus_dist = cam[c4d.CAMERAOBJECT_TARGETDISTANCE]
        
    elif cam.CheckType(1057516): #camera RS
        print('RS')
        fov_h = cam[c4d.RSCAMERAOBJECT_FOV].x
        fov_v = cam[c4d.RSCAMERAOBJECT_FOV].y  
        offset_x = cam[c4d.RSCAMERAOBJECT_SENSOR_SHIFT].x
        offset_y = cam[c4d.RSCAMERAOBJECT_SENSOR_SHIFT].y
        
        focus_dist = cam[c4d.RSCAMERAOBJECT_FOCUS_DISTANCE]
        
          
    else:
        print(f"{cam.GetName()} : not a standard camera")
    
    print(fov_h,fov_v)
    print(offset_x,offset_y)
    print(focus_dist)

if __name__ == '__main__':
    main()