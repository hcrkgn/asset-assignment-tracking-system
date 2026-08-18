import io

import qrcode


def generate_asset_qr(asset_id):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(f"ASSET:{asset_id}")
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    return output