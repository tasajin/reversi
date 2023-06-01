import tkinter
import tkinter.messagebox

squares = 8
canvas_size = 600
masu_size = canvas_size // squares

back_color = 'green'
next_color = 'yellow'

player_1 = 0
player_1_color = 'white'
player_2 = 1
player_2_color = 'black'



class reversi():
    def __init__(self, master):
        self.master = master
        self.player = player_1
        self.board = None
        self.color ={player_1:player_1_color,player_2:player_2_color}

        self.board_create()
        self.click()

    def board_create(self):
        self.canvas = tkinter.Canvas(
            self.master,
            bg=back_color,
            width=canvas_size+1,
            height=canvas_size+1,
            highlightthickness=0
        )
        self.canvas.pack(padx=10,pady=10)

        for y in range(squares):
            for x in range(squares):
                xs = x * masu_size
                xe = (x + 1) * masu_size
                ys = y * masu_size
                ye = (y + 1) * masu_size
                
                tag_name = 'square_' + str(x) + '_' + str(y)
                self.canvas.create_rectangle(
                    xs, ys,
                    xe, ye,
                    tag=tag_name
                )

        self.board = [[None] * squares for i in range(squares)]

        
        isi_4_4_x = squares // 2
        isi_4_4_y = squares // 2
        isi_5_5_x = squares // 2 - 1
        isi_5_5_y = squares // 2 - 1

        player_1_pos = (
            (isi_4_4_x, isi_4_4_y),
            (isi_5_5_x, isi_5_5_y)
        )

        for x, y in player_1_pos:
            self.isi(x, y, self.color[player_1])

        isi_4_5_x = squares // 2 - 1
        isi_4_5_y = squares // 2
        isi_5_4_x = squares // 2
        isi_5_4_y = squares // 2 - 1

        player_2_pos = (
            (isi_4_5_x, isi_4_5_y),
            (isi_5_4_x, isi_5_4_y)
        )

        for x, y in player_2_pos:
            self.isi(x, y, self.color[player_2])

        aki = self.masu_none()
        self.aki_masu(aki)
        

    def isi(self, x, y, color):

        center_x = (x + 0.5) * masu_size
        center_y = (y + 0.5) * masu_size

        xs = center_x - (masu_size * 0.8) // 2
        ys = center_y - (masu_size * 0.8) // 2
        xe = center_x + (masu_size * 0.8) // 2
        ye = center_y + (masu_size * 0.8) // 2
        
        tag_name = 'isi_' + str(x) + '_' + str(y)
        self.canvas.create_oval(
            xs, ys,
            xe, ye,
            fill=color,
            tag=tag_name
        )

        self.board[y][x] = color

    def click(self):
        self.canvas.bind('<Button-1>', self.click_masu)

    def masu_none(self):

        aki = []

        for y in range(squares):
            for x in range(squares):
                if self.check(x, y):
                    aki.append((x, y))
        return aki

    def check(self, x, y):
        if self.board[y][x] != None:
            return False

        if self.player == player_1:
            other = player_2
        else:
            other = player_1

        for j in range(-1, 2):
            for i in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if x + i < 0 or x + i >= squares or y + j < 0 or y + j >= squares:
                    continue
                if self.board[y + j][x + i] != self.color[other]:
                    continue
                for s in range(2, squares):
                    if x + i * s >= 0 and x + i * s < squares and y + j * s >= 0 and y + j * s < squares:
                        if self.board[y + j * s][x + i * s] == None:
                            break
                        if self.board[y + j * s][x + i * s] == self.color[self.player]:
                            return True
        return False


    def click_masu(self,event):
        x = event.x // masu_size
        y = event.y // masu_size

        if self.check(x,y):
            self.isi_set(x, y, self.color[self.player])
        
    def aki_masu(self, aki):
        for y in range(squares):
            for x in range(squares):
                tag_name = 'square_' + str(x) + '_' + str(y)
                if (x, y) in aki:
                    self.canvas.itemconfig(
                        tag_name,
                        fill=next_color
                    )

                else:
                    self.canvas.itemconfig(
                        tag_name,
                        fill=back_color
                    )
                    
    def isi_set(self, x, y, color):
        self.reverse(x, y)
        self.isi(x, y, color)

        self.turn()
        
        aki = self.masu_none()
        if not aki:
            self.turn()
            aki = self.masu_none()
            if not aki:
                self.result()
            return
        self.aki_masu(aki)


    def reverse(self, x, y):
        if self.board[y][x] != None:
            return
        if self.player == player_2:
            other = player_1
        else:
            other = player_2
        for j in range(-1, 2):
            for i in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if x + i < 0 or x + i >= squares or y + j < 0 or y + j >= squares:
                    continue
                if self.board[y + j][x + i] != self.color[other]:
                    continue
                for s in range(2, squares):
                    if x + i * s >= 0 and x + i * s < squares and y + j * s >= 0 and y + j * s < squares:
                        if self.board[y + j * s][x + i * s] == None:
                            break
                        if self.board[y + j * s][x + i * s] == self.color[self.player]:
                            for n in range(1, s):
                                self.board[y + j * n][x + i * n] = self.color[self.player]
                                tag_name = 'isi_' + str(x + i * n) + '_' + str(y + j * n)
                                self.canvas.itemconfig(tag_name, fill=self.color[self.player])
                            break

    def turn(self):
        before_player = self.player

        if self.player == player_1:
            self.player = player_2
        else:
            self.player = player_1

        aki = self.masu_none()

        if not aki:
            self.player = before_player
            aki = self.masu_none()
            self.player = before_player
            if not aki:
                self.player = None
                self.result()
            else:
                tkinter.messagebox.showinfo('スキップ', '手番がスキップされました')

    def result(self):
        num_player_1 = 0
        num_player_2 = 0

        for y in range(squares):
            for x in range(squares):
                if self.board[y][x] == player_1_color:
                    num_player_1 += 1
                elif self.board[y][x] == player_2_color:
                    num_player_2 += 1

        if num_player_1 > num_player_2:
            tkinter.messagebox.showinfo('結果', '白：' + str(num_player_1) + '・黒：' + str(num_player_2) + '\n白：プレイヤー１の勝利')
        elif num_player_2 > num_player_1:
            tkinter.messagebox.showinfo('結果', '白：' + str(num_player_1) + '・黒：' + str(num_player_2) + '\n黒：プレイヤー２の勝利')
        else:
            tkinter.messagebox.showinfo('結果', '引き分け')

root = tkinter.Tk()
root.title('reversi')
reversi(root)
root.mainloop()