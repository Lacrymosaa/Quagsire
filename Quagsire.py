import sys
import math
from itertools import product
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel
)
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtCore import Qt

class VoltorbFlipSolver:
    def __init__(self, row_sums, row_bombs, col_sums, col_bombs, fixed=None):
        self.N = 5
        self.row_sums = row_sums
        self.row_bombs = row_bombs
        self.col_sums = col_sums
        self.col_bombs = col_bombs
        self.fixed = fixed if fixed else [[None]*self.N for _ in range(self.N)]
        self.solutions = []
        self.row_candidates = [self._gen_row_candidates(r) for r in range(self.N)]

    def _gen_row_candidates(self, r):
        candidates = []
        def helper(c, current, ssum, sbomb):
            if c == self.N:
                if ssum == self.row_sums[r] and sbomb == self.row_bombs[r]:
                    candidates.append(current.copy())
                return
            fv = self.fixed[r][c]
            vals = [fv] if fv is not None else [1, 2, 3, 'B']
            for v in vals:
                a_sum = 0 if v == 'B' else v
                a_bomb = 1 if v == 'B' else 0
                if ssum + a_sum > self.row_sums[r] or sbomb + a_bomb > self.row_bombs[r]: continue
                current.append(v)
                helper(c+1, current, ssum+a_sum, sbomb+a_bomb)
                current.pop()
        helper(0, [], 0, 0)
        return candidates

    def solve(self):
        N = self.N
        col_sum_acc = [0]*N
        col_bomb_acc = [0]*N
        board = [None]*N
        def backtrack_row(r):
            if r == N:
                if all(col_sum_acc[j] == self.col_sums[j] and col_bomb_acc[j] == self.col_bombs[j] for j in range(N)):
                    self.solutions.append([row.copy() for row in board])
                return
            for rowcand in self.row_candidates[r]:
                valid = True
                for j, v in enumerate(rowcand):
                    a_sum = 0 if v == 'B' else v
                    a_bomb = 1 if v == 'B' else 0
                    if col_sum_acc[j] + a_sum > self.col_sums[j] or col_bomb_acc[j] + a_bomb > self.col_bombs[j]:
                        valid = False; break
                if not valid: continue
                board[r] = rowcand
                for j, v in enumerate(rowcand):
                    col_sum_acc[j] += 0 if v == 'B' else v
                    col_bomb_acc[j] += 1 if v == 'B' else 0
                backtrack_row(r+1)
                for j, v in enumerate(rowcand):
                    col_sum_acc[j] -= 0 if v == 'B' else v
                    col_bomb_acc[j] -= 1 if v == 'B' else 0
        backtrack_row(0)
        return self.solutions

    def probabilities(self):
        total = len(self.solutions)
        if total == 0: return None
        probs = [[{'1':0,'2':0,'3':0,'B':0} for _ in range(self.N)] for _ in range(self.N)]
        for sol in self.solutions:
            for i, j in product(range(self.N), repeat=2):
                probs[i][j][str(sol[i][j])] += 1
        for i, j in product(range(self.N), repeat=2):
            for k in probs[i][j]: probs[i][j][k] /= total
        return probs

class Quagsire(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quagsire")
        self.setWindowIcon(QIcon("quag.ico"))
        self.resize(400, 400)
        layout = QVBoxLayout(); self.setLayout(layout)

        self.grid = QTableWidget(6, 6)
        self.grid.horizontalHeader().setVisible(False)
        self.grid.verticalHeader().setVisible(False)
        self.grid.setFont(QFont('Arial', 12)); layout.addWidget(self.grid)

        btn_layout = QHBoxLayout()
        self.btn_solve = QPushButton("Solve"); self.btn_solve.clicked.connect(self.on_solve)
        self.btn_clear = QPushButton("Clear"); self.btn_clear.clicked.connect(self.on_clear)
        btn_layout.addWidget(self.btn_solve); btn_layout.addWidget(self.btn_clear)
        layout.addLayout(btn_layout)

        self.lbl_entropy = QLabel(""); self.lbl_entropy.setFont(QFont('Arial', 11, QFont.Bold))
        self.lbl_points = QLabel(""); self.lbl_points.setFont(QFont('Arial', 11, QFont.Bold))
        layout.addWidget(self.lbl_entropy); layout.addWidget(self.lbl_points)

        for i in range(6):
            for j in range(6):
                item = QTableWidgetItem(); item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
                item.setBackground(QColor('#E0E0E0') if i<5 and j<5 else QColor('#D0D0D0'))
                self.grid.setItem(i, j, item)
        self.grid.resizeColumnsToContents(); self.grid.resizeRowsToContents()

    def on_clear(self):
        for i in range(6):
            for j in range(6):
                item = self.grid.item(i, j); item.setText("")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
                item.setBackground(QColor('#E0E0E0') if i<5 and j<5 else QColor('#D0D0D0'))
        self.lbl_entropy.setText("")
        self.lbl_points.setText("")
        self.grid.resizeColumnsToContents(); self.grid.resizeRowsToContents()

    def on_solve(self):
        row_sums, row_bombs = [], []
        for i in range(5):
            txt = self.grid.item(i,5).text().strip()
            try: s,b = map(int, txt.split(','))
            except: s,b = 0,0
            row_sums.append(s); row_bombs.append(b)
        col_sums, col_bombs = [], []
        for j in range(5):
            txt = self.grid.item(5,j).text().strip()
            try: s,b = map(int, txt.split(','))
            except: s,b = 0,0
            col_sums.append(s); col_bombs.append(b)
        fixed = [[None]*5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                txt = self.grid.item(i,j).text().strip().upper()
                if txt in ('1','2','3'): fixed[i][j] = int(txt)
                elif txt in ('B','X'): fixed[i][j] = 'B'

        solver = VoltorbFlipSolver(row_sums, row_bombs, col_sums, col_bombs, fixed)
        solver.solve(); probs = solver.probabilities()

        best_entropy = None; best_h = -1
        best_point = None; best_score = -math.inf

        for i in range(5):
            for j in range(5):
                cell = self.grid.item(i,j)
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
                fv = fixed[i][j]
                if fv is not None:
                    cell.setText(str(fv))
                    cell.setBackground(QColor('#90EE90') if fv!='B' else QColor('#F08080'))
                    continue
                if probs is None:
                    cell.setText('X'); cell.setBackground(QColor('#F08080'))
                else:
                    p = probs[i][j]
                    cell.setText(f"2:{p['2']:.0%}\n3:{p['3']:.0%}\nB:{p['B']:.0%}")
                    base = QColor('#E0E0E0')
                    if p['B']==1: base = QColor('#F08080')
                    elif p['2']==1 or p['3']==1: base = QColor('#90EE90')
                    cell.setBackground(base)
                    ps = [p['1'], p['2'], p['3'], p['B']]
                    h = -sum(v*math.log(v) for v in ps if v>0)
                    if h > best_h:
                        best_h = h; best_entropy = (i,j)
                    score = (p['2'] + p['3']) - p['B']
                    if score > best_score:
                        best_score = score; best_point = (i,j)

        if best_entropy:
            i,j = best_entropy; self.grid.item(i,j).setBackground(QColor('#87CEEB'))
            self.lbl_entropy.setText(f"Suggestion to Reduce Variability: {i+1},{j+1}")
        else:
            self.lbl_entropy.setText("No Suggestions")
        if best_point:
            i,j = best_point; self.grid.item(i,j).setBackground(QColor('#FFD700'))
            self.lbl_points.setText(f"Suggestion to Point: {i+1},{j+1}")
        else:
            self.lbl_points.setText("No Suggestions")

        self.grid.resizeColumnsToContents(); self.grid.resizeRowsToContents()


def main():
    app = QApplication(sys.argv); w = Quagsire(); w.show(); sys.exit(app.exec_())

if __name__ == '__main__':
    main()
