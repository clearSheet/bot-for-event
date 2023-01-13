import asyncio
from PIL import Image, ImageDraw, ImageFont

async def generate(user_id: str,
                   user_name: str,
                   position_and_company_user: str,
                   user_login: str,
                   user_status: str):
    background_im = Image.open('data/BG.jpg')
    photo = Image.open(f'data/user_photos/{user_id}_photo.jpg')

    photo_size = photo.size
    # left_top_position = (120, 155)
    # left_down_position = (120, 1210)
    # right_top_position = (1110, 155)
    # right_down_position = (1110, 1210)

    width = 990  # Ширина
    height = 1055  # 1055  # Высота

    photo_width = photo_size[0]
    photo_height = photo_size[1]

    print(photo_size)
    print(str(width) + ' ' + str(height))

    if photo_height > height or photo_width > width:
        photo = photo.crop(((photo_width - width) // 2,
                         (photo_height - height) // 2,
                         (photo_width + width) // 2,
                         (photo_height + height) // 2))
    else:
        photo = photo.resize((int((photo_width + width) // 2), int((photo_height + height) // 2)))

    photo_size = photo.size

    photo_width = photo_size[0]
    photo_height = photo_size[1]

    x = ((width - photo_width) / 2) + 120
    y = ((height - photo_height) / 2) + 155

    card = background_im.copy()

    card.paste(photo, (int(x), int(y)))

    font = ImageFont.truetype(font='data/arial.ttf', size=50)

    drawing = ImageDraw.Draw(card)

    drawing.text(
                (140, 1240),
                f'{user_name}',
                font=font,
                fill=('#FFFFFF')
            )

    drawing.text(
        (140, 1290),
        f'{position_and_company_user}',
        font=font,
        fill=('#FFFFFF')
    )

    drawing.text(
        (140, 1345),
        f'TG: @{user_login}',
        font=font,
        fill=('#FFFFFF')
    )

    drawing.text(
        (140, 1400),
        f'{user_status}',
        font=font,
        fill=('#FF6600')
    )



    card.save(f'data/user_profiles/{user_id}_profile.jpg', quality=100)

    background_im.close()
    photo.close()

# asyncio.run(generate(user_name='Иван Анатольевич',
#                      position_and_company_user='Belarus company, Builder',
#                      user_id='225726820',
#                      user_login='wooziee',
#                      user_status='asda,lsdnaslkjdnajklndaljkdaljksdalkdn'))
# asyncio.run(generate(user_name='1', position_and_company_user='Belarus ', user_id='185974961',user_login='@asdasd', user_status='asdasdaa'))