from django.conf import settings


def google_analytics(request):
    """
    DEBUGがFalseの時にsettings.pyに設定したトラッキングIDを取得
    """
    ga_tracking_id = getattr(settings, 'GOOGLE_ANALYTICS_TRACKING_ID', False)
    """
    テンプレートタグで'GOOGLE_ANALYTICS_TRACKING_ID'という変数を
    使えるようにする
    """
    if not settings.DEBUG and ga_tracking_id:
        return {
            'GOOGLE_ANALYTICS_TRACKING_ID': ga_tracking_id,
        }
    return {}