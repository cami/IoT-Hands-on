# Vol.000 Raspberry Piセットアップ

## 1．準備するもの

### 必須

* [Raspberry Pi 3 Model B](https://www.amazon.co.jp/dp/B01CSFZ4JG)
* [micro SDカード（4GB以上が好ましい）](https://www.amazon.co.jp/dp/B00BLHWYWS)
* [USB電源（5V2.5A以上）](https://www.amazon.co.jp/dp/B01N8ZIJL8)


### 任意

* ディスプレイ（HDMI接続）
* マウス、キーボード
* スピーカー
* Raspberry Piケース
* ヒートシンク（Raspberry PiのICチップに貼り付ける）


### PC環境

* ターミナルソフト
  * Windows: [TeraTerm](https://ja.osdn.net/projects/ttssh2/)
  * macOS: ターミナル（ビルドイン）
* インターネット接続（WiFi / 有線LAN）


## 2. 環境構築

### OSのインストール

RaspbianのOSイメージを以下のURLからダウンロードしてmicroSDに書き込む。
キーボード、マウスで操作するGUI環境が必要な場合は Desktop版、
別のPCからのみ制御する場合は Lite版をダウンロードする。

https://www.raspberrypi.org/downloads/raspbian

microSDへの書き込み方は以下のURLを参照。

http://igarashi-systems.com/sample/translation/raspberry-pi/installation/install-image.html


### Raspberry Piの起動

* microSDをRaspberry Piに挿す
* マウス、キーボード、ディスプレイをRaspberry Piにつなぐ
* USB電源をRaspberry Piにつなぐ


### WiFiに接続

Raspberry Piでターミナルを開き、テキストエディタでWiFiの設定ファイルを開く。
```
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```


設定ファイルを以下の内容にする。SSID、PASSWORDは適切な値に置き換える。

```con
country=JP
ctrl_interface=DIR/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="SSID"
    psk="PASSWORD"
}
```


### パッケージのインストール

下記コマンドをRaspberryPi上で実行し、OSをアップグレードして、必要なツール、ライブラリをインストールする。

```
$ sudo apt update
$ sudo apt -y upgrade
$ sudo apt install -y git
$ sudo apt install -y python-pip
$ sudo apt install -y python3-pip
$ pip3 install picamera
$ pip3 install RPi.GPIO
```


### SSHサーバを有効にする

```
$ sudo raspi-config nonint do_ssh 0
```


### PiCameraを有効にする

```
$ sudo raspi-config
```

`5 Interfacing Options` を選択する。
`P1 Camera` を選択する。
`<Yes>` を選択する。
`<Ok>` を選択する。
`<Finish>` を選択する。