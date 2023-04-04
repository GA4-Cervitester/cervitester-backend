def getUserType(user):
    if hasattr(user, 'patient') and user.patient is not None:
        return 'patient'
    if hasattr(user, 'doctor') and user.doctor is not None:
        return 'doctor'
    if hasattr(user, 'admin') and user.admin is not None:
        return 'admin'
