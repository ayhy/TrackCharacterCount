TrackCharacterCount（今日何文字書いた？）
====

* A python snippet to track daily writing record of file(s) in character count.
* 毎日定時実行してテキストファイルの文字数をカウントし、昨日の文字数から差分を出して執筆ペースを把握するためのスクリプトです。

## Prerequisite
* Python 3.x系

## Usage
* tasklog_formatをコピーして対象のファイルを設定した記録用のファイルをつくる
* タスクスケジューラ（windows）、launchd(mac)、cron(linux)などの定時実行機能に以下のコマンドを毎日実行するように設定する。自分が確実に執筆していない時間を選ぶと安全です。
```
path/to/python/python.exe path/to/tracker.py  path/to/log.txt
```
* できるだけ毎日書きましょう。

## Notes:
* 対象のファイルをdropboxなどで同期している場合、同期タイミングによっては正確な結果にならないことがあります。
* プロットが固まり始めた段階～初稿を上げるまでの過程を想定したツールです。ログ・設定ファイルに入れておくdeadlineの日付は、改稿・校正にかかる時間を含めて余裕をもって設定したほうがよいでしょう。
* "補稿"は、コメントアウト記法`<!--コメント-->`か、`/*コメント*/`で退避させた没稿、プロットなどを指します。使わない人は無視してください。


## Licence
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author
[ayhy](https://github.com/ayhy)