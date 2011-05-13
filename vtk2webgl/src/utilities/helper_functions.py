#Extensions supported by 3D models.
ALLOWED_EXTENSIONS = set(['vtk'])


def allowed_files(filename):
    """
    This function control which files are allowed to submit.
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS