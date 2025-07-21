import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

#Supprimer les matériaux créé et sélectionner le neutre "photomaillage_SITG"

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    for o in op.GetChildren():
        fn_img = o.GetName()[:-4]+'.jpg'
        mat = c4d.BaseMaterial(c4d.Mmaterial)
        mat.SetName(o.GetName()[:-4])
        doc.InsertMaterial(mat)
        shd = c4d.BaseShader(c4d.Xbitmap)
        shd[c4d.BITMAPSHADER_FILENAME] = fn_img
        mat.InsertShader(shd)
        mat[c4d.MATERIAL_USE_REFLECTION] = False
        mat[c4d.MATERIAL_COLOR_MODEL]=1
        mat[c4d.MATERIAL_COLOR_SHADER] = shd
        mat.Update(True, True)
        
        tag = o.GetTag(c4d.Ttexture)
        if tag :
            tag[c4d.TEXTURETAG_MATERIAL] = mat
    c4d.EventAdd()


if __name__ == '__main__':
    main()