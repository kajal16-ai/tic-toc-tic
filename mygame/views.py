from django.shortcuts import render,redirect

# Create your views here.

def home(request):
    if request.method == 'POST' and 'reset' in request.POST:
        request.session['board'] == [["","",""],["","",""],["","",""]]
        request.session['player'] = 'x'
        request.session['winner'] = ""
        return redirect('home')

    board = request.session.get('board',[["","",""],["","",""],["","",""]])
    current_player = request.session.get('player','x')
    winner = request.session.get('winner',"")

    if request.method == 'POST' and 'move' in request.POST and not winner:
        pos = request.POST['move'].split('-')
        row,col = int(pos[0]), int(pos[1])
        if board[row][col] == "":
            board[row][col] = current_player
            winner = check_winner(board)
            if winner:
                request.session['winner'] = winner
            else:
                current_player = 'O' if current_player == 'X' else 'X'
                request.session['player'] = current_player
            request.session['board'] = board

    message = ""
    if winner:
        message = f"🎉 Player {winner} wins!"
    elif all(cell for row in board for cell in row):
        message = "🤝 It's a draw!"

    return render(request, 'home.html', {
        'board': board,
        'current_player': current_player,
        'winner': winner,
        'message': message,
    })

def check_winner(board):
    win_combinations = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]

    for line in win_combinations:
        if line[0] != "" and line.count(line[0]) == 3:
            return line[0]
    return ""