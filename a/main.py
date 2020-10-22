import pyxel
from enum import Enum
import random

# 状態の列挙体クラス
class State(Enum):
    STANDING      = 1 # 地面に立っている
    JUMPING       = 2 # ジャンプ中
    AERIAL_ATTACK = 3 # 空中攻撃中
    RECOVERY      = 4 # 硬直中

class App:
    GROUND_Y = 100 # 地面の座標
    def __init__(self):
        pyxel.init(160, 120, fps=60)
        self.init()
        pyxel.run(self.update, self.draw)
    def init(self):
        #pyxel.image(0).load(0, 0, "cat.png")
        pyxel.image(0).load(0, 0, "img/cat.png")
        # ニャンコ変数の初期化
        self.x = 72
        self.y = self.GROUND_Y - 16
        self.vy = 0 # Y方向の速度
        self.gravity = 0.05 # 重力
        self.state = State.STANDING
        #self.is_jumping = False # ジャンプ中かどうか
        #self.is_aerial_attack = False # 空中攻撃
        self.recovery_frame = 0
    def update(self):
        # キー入力判定
        self.input_key()

        # 加速度更新
        self.vy += self.gravity
        # 速度を更新
        self.y += self.vy

        # ニャンコを地面に着地させる
        if self.y > self.GROUND_Y - 16:
            self.y = self.GROUND_Y - 16
            if self.state == State.AERIAL_ATTACK:
                self.state = State.RECOVERY
                self.recovery_frame = 20 # 20フレーム間硬直する
            elif self.state == State.JUMPING:
                # 通常の着地
                self.state = State.STANDING
            #self.is_jumping = False # 着地した
            #self.is_aerial_attack = False
    # キー入力
    def input_key(self):
        if self.state == State.STANDING:
            if pyxel.btnp(pyxel.KEY_SPACE):
                # ジャンプする
                self.vy = -2
                self.state = State.JUMPING
        elif self.state == State.JUMPING:
            if pyxel.btnp(pyxel.KEY_SPACE):
                # 空中攻撃を開始する
                self.vy = 3
                self.state = State.AERIAL_ATTACK
        elif self.state == State.AERIAL_ATTACK:
            # 特に何もしない
            pass
        elif self.state == State.RECOVERY:
            if self.recovery_frame > 0:
                # 硬直中
                self.recovery_frame -= 1
            else:
                # 硬直終了
                self.state = State.STANDING


    def draw(self):
        pyxel.cls(0)

        # 地面を描画
        pyxel.rect(0, self.GROUND_Y, pyxel.width, pyxel.height, 4)

        px = self.x
        py = self.y
        if self.state == State.RECOVERY:
            if self.recovery_frame%2 == 0:
                py += self.recovery_frame/4

        pyxel.blt(px, py, 0, 0, 0, 16, 16, 5)

App()