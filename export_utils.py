import csv
import io
import base64
from datetime import datetime


def generate_csv_content(data):
    videos = data['videos']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

    writer.writerow(['视频名称', '点赞数', '评论数', '分享数', '总互动数'])

    for i in range(len(videos)):
        total = likes[i] + comments[i] + shares[i]
        writer.writerow([
            videos[i],
            likes[i],
            comments[i],
            shares[i],
            total
        ])

    total_likes = sum(likes)
    total_comments = sum(comments)
    total_shares = sum(shares)
    grand_total = total_likes + total_comments + total_shares

    writer.writerow([])
    writer.writerow(['合计', total_likes, total_comments, total_shares, grand_total])

    return output.getvalue()


def create_download_link(csv_content, filename_prefix='互动数据'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{filename_prefix}_{timestamp}.csv'

    csv_bytes = csv_content.encode('utf-8-sig')
    b64 = base64.b64encode(csv_bytes).decode()

    return dict(
        content=b64,
        filename=filename,
        type='text/csv',
        base64=True
    )


def export_data_to_csv(data, period_label='今日'):
    csv_content = generate_csv_content(data)
    return create_download_link(csv_content, f'互动数据_{period_label}')
