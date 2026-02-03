# narcissu_gba
## ソフトについて
2005年に同人サークル「ステージ☆なな」から公開されたゲーム「narcissu」を、GBAで動作させるための変換ツールです。<br>
本ツールは非公式であり、原作者・原サークル様とは一切関係ありません。


## 動作環境
### コンバータについて
Windows 10 以降での動作を想定しています。<br>
他の環境については検証していません。<br>
<br>
制作/検証に使用した作者のPC環境<br>
[![CPU-Z](https://valid.x86.fr/cache/banner/eidarj-2.png)](https://valid.x86.fr/eidarj)<br>


### 変換したROMについて
以下の環境でセーブ/ロード、クリアまでの動作は確認しました。
 - [mGBA 0.10.5  (Windows, 64bit, portable版)](https://mgba.io/downloads.html)
 - [ChisFlash V1.1 RTC Cart (EPICJOY製)](https://ja.aliexpress.com/item/1005010183225651.html)

※RTC対応カートリッジで動作確認を行っただけであり、本ROMがRTC機能を使用するわけではありません

## 基本的な使い方
 1. [Releasesから最新のnarcissu_gba.7zをダウンロード](https://github.com/Prince-of-sea/narcissu_gba/releases/latest)し、展開してください
 2. 「Narcissu_GBA_Converter.exe」を起動します
 3. 選択項目を確認し、「Convert」を押してください
 4. 進捗バーが100%になり、「変換が完了しました」という表示が出たら完了です

出力された`NarcissuGBA.gba`または`NarcissuGBA (no voice).gba`を、エミュレータ/フラッシュカートへ転送してください


## 注意事項など
### 仕様
 一部を除き、セーブ・ロードやオプションなどの基本的な部分は全て「終末の過ごし方GBA」を流用しています。<br>
 現時点で最初から最後まで全てのシナリオを読むことができますが、演出面では原作を再現しきれていない箇所がいくつかあります。
 - ボイス有無をタイトルから選べません
 - ループ効果音がループで再生されません
 - 効果音とボイスを同時に流すことができません
 - ウェイト時間が全体的に原作より若干短めです
 - メッセージ表示ではない、単純なボタン押下待ちにも改ページアイコンが表示されます
 - 「環境設定」→「音楽」の順番および内容が原作にあったサウンドモードと全く合致しません
 - Chapter選択画面とProductの選択肢がなく、読み終わるとそのまま次へ遷移する一本道仕様になっています
 - Productの文字の表示位置が本編と同じになっています、また文字数の関係で一部の改行だった場所を改ページにしました
 - 独自メニュー「変換情報」について、背景が切り替わる場面まで変換情報画面が表示されたままになります(「環境設定」→「画像」と同様の仕様)


### ライセンス
| GBA ROM側                          | license                                                |
| :--------------------------------- | :----------------------------------------------------- |
| 下記を除くGBAソースコード          | CC0                                                    |
| CULT-GBA and fixed Lorenzooone ver | [MIT](./src/c/game_core/libbios/lz77.s)                |
| libgba                             | [LGPL2.0](./src/c/game_core/libgba/libgba_license.txt) |
| crt0.s                             | [MPL2.0](./src/c/game_core/libgba/crt0.s)              |
| k12x10 font                        | Public domain                                          |

| コンバータ側             | license                                                                        |
| :----------------------- | :----------------------------------------------------------------------------- |
| Pythonソースコード全般   | [GPL2 or later](./src/python/converter/LICENSE)                                |
| arc_unpacker.exe         | [GPL3](./src/python/converter/tools/arc_unpacker/LICENSE.md)                   |
| gbfs.exe                 | [GPL3](./src/python/converter/tools/gbfs/COPYING)                              |
| grit.exe                 | [GPL2](./src/python/converter/tools/grit/license-gpl.txt)                      |
| sox.exe(および同梱のdll) | [GPL2](./src/python/converter/tools/sox/LICENSE.GPL.txt)                       |
| 源柔ゴシック             | [SIL](./src/python/converter/resources/fonts/GenJyuuGothic-Monospace-Bold.ttf) |

 - Pythonで利用しているライブラリのライセンスは、コンバータ内メニューの「このソフトについて」→「ライセンス」で確認できます
 - narcissuのゲーム本体(nana24.exe)については「はじめに.txt」に以下の内容が書いてあったので、Releasesに同梱させていただいています
```
★転載等について…

こちらの「Ｎａｒｃｉｓｓｕ」Web版につきましては、
アーカイブ内容の改変等をしない限り、
転載は自由となっております。
```


### お約束
 本ツールの使用において生じた問題や不利益などについて、製作者は一切その責任を負わないものとします。<br>
 また、それらの問題を他のツールの製作者様やサークル様に問い合わせるのは**絶対にやめてください。**<br>
