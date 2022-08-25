from backend.models import ConfirmEmailToken


def account_activation(email: str, token: str) -> dict:
    token = ConfirmEmailToken.objects.filter(user__email=email,
                                             key=token).first()
    if token:
        token.user.is_active = True
        token.user.save()
        token.delete()
        return {'Status': True}
    else:
        return {'Status': False, 'Errors': 'Токен или email указан неправильно'}
