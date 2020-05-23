import vk_api

vk_session = vk_api.VkApi('TEL','PAS')
vk_session.auth()

vk = vk_session.get_api()

# Функция для вычисление самой часто встречающейся тематики
#   и количества её встречаний так сказать
def get_data_about_favorite(groups_topics):
    set_topics = list(set(groups_topics))
    count_favorite_topic = 0
    favorite_topic = None
    for topic in set_topics:
        temp = groups_topics.count(topic)
        if temp > count_favorite_topic:
            count_favorite_topic = temp
            favorite_topic = topic
    return [favorite_topic, count_favorite_topic]

MY_ID = '152858538'

# список тематик моих групп без "Открытая группа" "Закрытая группа" и без None
my_groups_topics = list(list(filter(None,map(lambda x: x['activity'] if 'activity' in x and x['activity'] != "Открытая группа" and x['activity'] != "Закрытая группа" else None,
                            vk.groups.get(user_id = MY_ID, extended = True, fields = 'activity')['items']))))

# Получаю свою любимую тему и на сколько групп с такой темой я подписан
data_about_me = get_data_about_favorite(my_groups_topics)
MY_FAVORITE_TOPIC = data_about_me[0]
# Вычисляю процент моиъ подписок на группу с любимой тематикой
#   по отношению ко всем подпискам. И если у моего друга будет такая же любимая
#   тематика и процент его подписок на группу с данной тематикой будет
#   больше либо равен (MIN_PERCENT - 7), то он считается близким по духу
MIN_PERCENT = round(data_about_me[1]/len(my_groups_topics) * 100) - 7

# Получаю id всех своих друзей
my_friends_id = vk.friends.get(user_id = MY_ID)['items']

# Заготваливаю итоговый список, где будут лежать id близких по духу друхей
result = []
for friend_id in my_friends_id:
    # Может возникнуть ошибка, что пользователь удалил страницу
    try:
        # Здесь мы аналогично тому, как получал инфу о группах для себя
        #   получаем список тем групп у друга
        friend_groups_topics = list(list(filter(None,map(lambda x: x['activity'] if 'activity' in x and x['activity'] != "Открытая группа" and x['activity'] != "Закрытая группа" else None,
                                vk.groups.get(user_id = str(friend_id), extended = True, fields = 'activity')['items']))))
    except vk_api.exceptions.ApiError:
        continue
    # Если друг закрыл информацию о своих группах, то длинна этого списка будет 0
    #   соотвественно мы не сможем узнать его любимые тематикии(пропускаем остальное тело)
    if len(friend_groups_topics) == 0: continue

    # Получаем любимую тему друга и количество его подписок на группы с такой темой
    data_about_friend = get_data_about_favorite(friend_groups_topics)
    friend_favorite_topic = data_about_friend[0]
    # Так же высчитываю процент от общего количества
    friend_percent = round(data_about_friend[1]/len(friend_groups_topics) * 100) - 7

    # И если он удовлетворяет условиям: (MIN_PERCENT - 7) и наши любимые темы совпадают,
    #   то мы заносим его id в итоговый список
    if friend_percent >= MIN_PERCENT and friend_favorite_topic == MY_FAVORITE_TOPIC:
        result.append(friend_id)
print(result)