#そのままだと使えない SCN003.binの文字列開始直後とかに挟む

def write_binary(filename: str, max_number: int, step_hex: int = 0x01):
    if not (0 <= max_number <= 99999):
        raise ValueError("max_number must be between 0 and 99999")

    with open(filename, "wb") as f:
        for i in range(max_number + 1):
            # 全角5桁ゼロ埋め（10進）
            zenkaku = f"{i:05d}".translate(
                str.maketrans("0123456789", "０１２３４５６７８９")
            )

            # 半角4桁・16進・0x14ずつ加算
            value = (i + 1) * step_hex
            hankaku_hex = f"{value:04X}"

            block = (
                b"_r" +
                b"\x00" +
                zenkaku.encode("utf-8") +
                b"\x00" +
                hankaku_hex.encode("ascii") +
                b"\x00"
            )

            f.write(block)


# ===== 使用例 =====
if __name__ == "__main__":
    write_binary("output.bin", 30000)
