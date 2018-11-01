# Vol.001 焦電センサー

## 1. 準備するもの

### 必須

* [Vol.000でセットアップしたRaspberry Pi](../vol000-raspberrypi-setup/README.md)（今回はセットアップ済みのRaspberry Piを用意）
* [焦電センサ（SB412A）](http://akizukidenshi.com/catalog/g/gM-09002)
* [PiCamera](https://www.amazon.co.jp/dp/B01D1D0DJ0)
* LED
* 抵抗
  * [100Ω x 1個](http://akizukidenshi.com/catalog/g/gR-25101)
  * [150Ω x 1個](http://akizukidenshi.com/catalog/g/gR-25151)
  * [10kΩ x 1個](http://akizukidenshi.com/catalog/g/gR-25103)
* NPN型トランジスタ [2SC1815](http://akizukidenshi.com/catalog/g/gI-04268)
* ジャンパワイヤ
  * [オスーメス 3本](http://akizukidenshi.com/catalog/g/gC-08932)
  * [オスーオス 適量](http://akizukidenshi.com/catalog/g/gC-05371)


### 任意

* モバイルバッテリ（離れた場所にRaspberry Piを置く場合）


### PC環境

* Slackアカウント


## 2. 体験

キーボード、マウス、ディスプレイをRaspberryPiに接続せず、開発していきましょう！


### Exercise1「電子工作してみよう」

#### 焦電センサを使う

「人を検知したらLEDが光る」という単純な回路を作成してみましょう。

回路図

![回路図1](./docs/exercise1/schematic.png)


#### 仕組み

* 焦電センサが人（赤外線）を検知する
* 焦電センサのVoutがHighになる
* トランジスタがonとなり、LEDが点灯する

焦電センサの[データシート](http://akizukidenshi.com/catalog/g/gM-09002)を確認してみましょう。
「電源電圧(Vdd): 3.3V~12V、出力: 検出時(High)3V」とあります。

Raspberry Piのピンヘッダには 3.3V と 5V の電源出力ピンがあるため、3.3V の電源出力ピンを焦電センサの電源として使用することができます。

焦電センサからは3本のピンヘッダが出ています。真ん中は出力ピン Vout です。
![写真](./docs/exercise1/pyroelectric-sensor.jpg)

Raspberry Piの各GPIOの説明は以下を参照してください。
https://pinout.xyz


GPIO（汎用入出力）のピン配置
![GPIOのピン配置](./docs/exercise1/pinout.png)


人を検知した場合、Vout が High となり 3V が出力されます。人を検知してから、一定時間後（センサーに付いているボリュームで調整可能）

センサー反応のタイミングチャート
![timing-chart](./docs/exercise1/timing-chart.png)

<!-- コメントアウト
作成ツール: https://rawgit.com/osamutake/tchart-coffee/master/bin/editor-offline.html

手 _存在しない_____~存在する~~~~~~~~~_存在しない______________
Vout ______~~~~~~~~~~~~~~~~~~~~_____
GPIO =0=====X=1==================X=0===
-->


データシートにあるように、Voutは焦電センサの基板上の 20kΩ の抵抗を介して出力されているので、オームの法則より、約100μAの電流が出力されます。

この程度の電流ではLEDが明るく光らないため、NPN型トランジスタで増幅します。

NPN型トランジスタのベース端子に焦電センサの出力電流が流れ込むことにより、トランジスタがonとなりコレクタ端子とエミッタ端子が導通して、LEDに電流が流れるようになります。

トランジスタの増幅作用により、LEDにはベース端子に流れ込む電流の約100倍がコレクタ端子からエミッタ端子に流れます。

正しく動作すると、以下のように手や顔を近づけるとLEDが光ります。

![Exercise1 product](./docs/exercise1/product.jpg)


### Exercise2「Raspberry Piで焦電センサからデータを取得してみよう」

LEDを光らせる代わりに、Raspberry PiのGPIOを用いて焦電センサの出力状態（High, Low）を読み取ってみましょう。


#### Raspberry Piを起動する

* Raspberry Piにmicro SDカードが挿してあること確認して、USB電源をつないでください。

* Raspberry Piが起動したら、TeraTermを起動してログインします。

```
IPアドレス: Raspberry Piのケースに貼り付けてあるラベル
ユーザー名: pi
パスフレーズ: raspberry
```

![SSH](./docs/exercise2/ssh.png)


ログインが完了したら、このような画面が表示されます。


![login_ssh](./docs/exercise2/login-ssh.png)


#### 電子回路を作成する

以下の実体配線図を見ながら、つないでみてください。

![回路図2](./docs/exercise2/breadboard.png)


#### GPIOでデータを読み取る

GPIOから焦電センサの出力状態（High, Low）を読み取るソースコードをGitHubから取得します。

Raspberry Piで、以下のコマンドを実行しましょう。

```
$ git clone https://github.com/cami/IoT-Hands-on.git
```

取得したディレクトリの中の、vol001-pyroelectric-sensorというディレクトリに移動します。

Raspberry Piで、以下のコマンドを実行しましょう。

```
$ cd /home/pi/IoT-Hands-on/vol001-pyroelectric-sensor
```

このディレクトリの中に、motion_sensor.py というPythonファイルがありますので、実行してください。

```
$ python3 motion_sensor.py
```

成功すれば、人を検知すれば1、検知しなければ0が表示されるはずです。

![Exercise2 Python](./docs/exercise2/exec.png)


### Exercise3「人を検知したら写真を撮影してSlackに送信しよう」

最後に、人を検知したら写真を撮影することで、防犯カメラの役割を与えましょう。

今回は通知と閲覧を容易にするために、Slackに写真を送信しています。


#### PiCameraをRaspberryPiに装着する

写真を撮影するために、PiCameraをRaspberry Piに接続しましょう。コネクタが壊れやすいので気を付けてください。

![PiCamera on Raspberry Pi](./docs/exercise3/connect-picamera.jpg)


#### Slack APIのTokenを設定する

撮影した写真をSlackに投稿するために、Slack APIのTokenを設定します。Tokenは先ほど招待したSlackのワークスペースの `#general` チャンネルに記載してあります。

ご自分のSlackを使いたい場合は以下のページを参考にTokenを発行してください。Permission Scopeには`files.upload` を追加してください。https://qiita.com/ykhirao/items/3b19ee6a1458cfb4ba21


Raspberry Piで以下のコマンドを実行して`motion_detected_send_slack.py` ファイルを編集します。

```
$ nano /home/pi/IoT-Hands-on/vol001-pyroelectric-sensor/motion_detected_send_slack.py
```

22行目の以下の行を、Slack の `#general` チャンネルに投稿したTokenに置き換えます。

```python
TOKEN = 'xoxp-'
```


#### 電子回路を作成する

こちらの回路図を見ながら作成してみてください。

![回路図3](./docs/exercise3/schematic.png)

ブレッドボードへの配線は下記の通りになります。

![回路図3_ブレッドボード](./docs/exercise3/breadboard.png)


#### 実行する

Raspberry Piで、以下のコマンドを実行しましょう。人を検知したらSlackに写真が送られるはずです。

こちらのチャンネル [# security-camera](https://camico-kousaku-01.slack.com/messages/CDSC8F066/) で確認してみましょう！


```
$ python3 motion_detected_send_slack.py
```

Slackへの通知が完了したら、Slack APIのAPIリファレンスを参照しながら、Slackへのアップロードをカスタマイズしてみましょう。

[Slack API files.upload](https://api.slack.com/methods/files.upload)
