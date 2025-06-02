from category.models import CategoryKeyword, PredefinedCategoryKeyword

def suggest_category(user, description):
    if not description:
        return None

    keywords = CategoryKeyword.objects.filter(category__user=user)
    for kw in keywords.order_by('-priority'):
        if kw.is_exact_match and kw.keyword.lower() == description.lower():
            return kw.category
        elif not kw.is_exact_match and kw.keyword.lower() in description.lower():
            return kw.category

    predefined_keywords = PredefinedCategoryKeyword.objects.all()
    for pk in predefined_keywords.order_by('-priority'):
        if pk.is_exact_match and pk.keyword.lower() == description.lower():
            return pk.predefined_category
        elif not pk.is_exact_match and pk.keyword.lower() in description.lower():
            return pk.predefined_category

    return None
