from __future__ import division, print_function, unicode_literals, absolute_import

def transform_geom(geom=None):
    '''
    Requires GDAL. Accepts a Polygon or MultiPolygon geometry, and returns it transformed to a
    projection of GDA94/MGA zone 49 through 56, depending on the centroid.
    If the centroid lies outside the appropriate X coordinates, returns None instead.
    '''
    if hasattr(geom, 'centroid'):
        x = geom.centroid.x
        if x > 108 and x <= 114: srid = 28349
        elif x > 114 and x <= 120: srid = 28350
        elif x > 120 and x <= 126: srid = 28351
        elif x > 126 and x <= 132: srid = 28352
        elif x > 132 and x <= 138: srid = 28353
        elif x > 138 and x <= 144: srid = 28354
        elif x > 144 and x <= 150: srid = 28355
        elif x > 150 and x <= 156: srid = 28356
        else: return None
        return geom.transform(ct=srid, clone=True)
    else:
        return None

def check_user_role(user, role):
    '''
    Convenience function to test if the user has the role passed in (or is a superuser).
    '''
    if not (user.rolelink_set.filter(role=role) or user.is_superuser):
        return False
    else:
        return True
