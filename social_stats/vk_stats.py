import vk_api
from datetime import datetime

def get_vk_stats(token, group_id, start_date, end_date):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    group_id = int(group_id)  # Ensure group_id is an integer

    try:
        ts_from = datetime.strptime(start_date, '%Y-%m-%d').timestamp()
        ts_to = datetime.strptime(end_date, '%Y-%m-%d').timestamp()

        stats = vk.stats.get(
            group_id=abs(group_id),
            timestamp_from=ts_from,
            timestamp_to=ts_to
        )

        return stats
    except vk_api.exceptions.ApiError as e:
        print(f"An error occurred: {e}")

class VKStats:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = int(group_id)  # Ensure group_id is an integer

    def get_stats(self, start_date, end_date):
        return get_vk_stats(self.vk_api_key, self.group_id, start_date, end_date)

    def convert_stats_to_list(self, stats):
        data = []
        for stat in stats:
            date = datetime.fromtimestamp(stat['period_from']).strftime('%Y-%m-%d')
            visitors = stat.get('visitors', {})
            data.append({
                'date': date,
                'views': stat.get('views', 0),
                'likes': stat.get('likes', 0),
                'shares': stat.get('shares', 0),
                'comments': stat.get('comments', 0),
                'subscribers': stat.get('subscribed', 0) - stat.get('unsubscribed', 0),
                'visitors': visitors
            })

        return data
