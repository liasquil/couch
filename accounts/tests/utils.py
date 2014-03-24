from ..models import CustomUser, Language, LanguageSkill



def create_user(username, email, password=''):
    return CustomUser.objects.create(username=username, email=email, password=password)

def create_lang(name):
    return Language.objects.create(name=name)

def create_lang_skill(language, user, level):
    return LanguageSkill.objects.create(speaker_profile=user.profile, language=language, level=level)