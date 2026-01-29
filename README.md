# narcissu_gba
## ソフトについて
2005年に同人サークル「ステージ☆なな」から公開されたゲーム「narcissu」を、GBAで動作させるための変換ツールです。<br>
本ツールは非公式であり、原作者・原サークル様とは一切関係ありません。


## 動作環境
### コンバータについて
Windows 10 以降での動作を想定しています。<br>
他の環境については検証していません。

[制作/検証に使用した作者のPC環境]<br>
PCスペック: <br>
[![CPU-Z](https://valid.x86.fr/cache/banner/eidarj-2.png)](https://valid.x86.fr/eidarj)<br>


### 変換したROMについて
以下の環境でセーブ/ロード、クリアまでの動作は確認しました。
 - [mGBA 0.10.5  (Windows, 64bit, portable版)](https://mgba.io/downloads.html)
 - [ChisFlash V1.1 RTC Cart (EPICJOY製)](https://ja.aliexpress.com/item/1005010183225651.html)


## 基本的な使い方
 1. [Releasesから最新のnarcissu_gba.7zをダウンロード](https://github.com/Prince-of-sea/narcissu_gba/releases/latest)し、展開してください
 2. 「Narcissu_GBA_Converter.exe」を起動します
 3. ラジオボタンのどちらか一方を選択し、「Convert」を押してください
 4. 進捗バーが100%になり、「変換が完了しました」という表示が出たら完了です

出力された`NarcissuGBA.gba`または`NarcissuGBA (no voice).gba`を、エミュレータ/フラッシュカートへ転送してください


## 注意事項など
### 仕様
 シナリオ自体は最初から最後まで全て読むことができますが、演出面で原作を再現しきれていない箇所がいくつかあります。
 - ボイス有無をタイトルから選べません
 - ループ効果音がループで再生されません
 - 効果音とボイスを同時に流すことができません
 - ウェイト値が合っていません(全体的に原作より短め)
 - 単純なクリック待ち(だったところ)にも改ページアイコンが表示されます
 - 「環境設定」→「音楽」の順番および内容が原作のサウンドモードと全く合致しません
 - Chapterごとの選択画面がなく、読み終わるとそのまま次のChapterへ遷移します(Productも同様)
 - Productの文字の表示位置が本編と同じになっています、また文字数の関係で一部の改行だった場所が改ページになっています
 - 独自のBボタンメニュー「変換情報」について、背景が切り替わる場面まで変換情報画面が表示されたままになります(「環境設定」→「画像」と同様の仕様)


### ライセンス
| GBA ROM側                          | license                                                |
| :--------------------------------- | :----------------------------------------------------- |
| 下記を除くGBAソースコード          | CC0                                                    |
| libgba                             | [LGPL2.0](./src/c/game_core/libgba/libgba_license.txt) |
| CULT-GBA and fixed Lorenzooone ver | [MIT](./src/c/game_core/libbios/lz77.s)                |
| crt0.s                             | [MPL2.0](./src/c/game_core/libgba/crt0.s)              |

| コンバータ側           | license                                                                        |
| :--------------------- | :----------------------------------------------------------------------------- |
| Pythonソースコード全般 | [GPL2 or later](./src/python/converter/LICENSE)                                |
| 源柔ゴシック           | [SIL](./src/python/converter/resources/fonts/GenJyuuGothic-Monospace-Bold.ttf) |
| arc_unpacker.exe       | [GPL3](./src/python/converter/tools/arc_unpacker/LICENSE.md)                   |
| gbfs.exe               | [GPL3](./src/python/converter/tools/gbfs/COPYING)                              |
| grit.exe               | [GPL2](./src/python/converter/tools/grit/license-gpl.txt)                      |
| sox.exeおよび同梱のdll | [GPL2](./src/python/converter/tools/sox/LICENSE.GPL.txt)                       |

 - Pythonで利用しているライブラリのライセンスは、コンバータ内メニューの「このソフトについて」→「ライセンス」で確認できます
 - narcissuのゲーム本体(nana24.exe)については「はじめに.txt」に以下の内容が書いてあったので、Releasesに同梱させていただいています。
```
★転載等について…

こちらの「Ｎａｒｃｉｓｓｕ」Web版につきましては、
アーカイブ内容の改変等をしない限り、
転載は自由となっております。
```


### お約束
 本ツールの使用において生じた問題や不利益などについて、製作者は一切その責任を負わないものとします。<br>
 また、それらの問題を他のツールの製作者様やサークル様に問い合わせるのは**絶対にやめてください。**<br>
