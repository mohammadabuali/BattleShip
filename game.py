############################################################
# Imports
############################################################
import game_helper as gh
from ship import Ship
import copy
############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board.
        :param ships: A list of ships (of type Ship) that participate in the
            game.
        :return: A new Game object.
        """
        self.__board_size = board_size
        self.__ships = ships
        self.__bombs = {}
        self.__hit_ships = []

    def __play_one_round(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits and
             terminated ships)
        :return:
            (some constant you may want implement which represents) Game status :
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """
        hits = []
        num_terminated = 0
        target = gh.get_target(self.__board_size)
        starting_num = 3
        self.__bombs[target] = starting_num
        all_coor = []

        for ship_j in self.__ships:
            Ship.move(ship_j)

        for key in self.__bombs:
            if self.__bombs[key] > 0:
                for ship_i in self.__ships:
                    for i in Ship.coordinates(ship_i):
                        all_coor.append(i)
                    if Ship.hit(ship_i, key):
                        hits.append(key)
                        for i in hits:
                            self.__hit_ships.append(i)
                        bomb_dict = dict(self.__bombs)
                        if key in bomb_dict:
                            del bomb_dict[key]
                        self.__bombs = bomb_dict




            else:
                bomb_dict = dict(self.__bombs)
                del bomb_dict[key]
                self.__bombs = bomb_dict




        for i in self.__hit_ships:
            if i in all_coor:
                all_coor.remove(i)
        print(gh.board_to_string(self.__board_size, hits, self.__bombs, self.__hit_ships, all_coor))
        for key in self.__bombs:
            self.__bombs[key] -= 1

        for ship_k in self.__ships:
            if Ship.terminated(ship_k):
                for i in Ship.coordinates(ship_k):
                    if i in self.__hit_ships:
                        self.__hit_ships.remove(i)
                self.__ships.remove(ship_k)
                num_terminated += 1

        gh.report_turn(len(hits), num_terminated)




    def __repr__(self):
        """
        Return a string representation of the board's game.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)). The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board, mapping their
                coordinates to the number of remaining turns:
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        for key in self.__bombs:
            self.__bombs[key] += 1

        tup_repr = (self.__board_size, self.__bombs, self.__ships)
        return str(tup_repr)
    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        gh.report_legend()

        lst_check = []
        for ship_ran in self.__ships:
            for j in Ship.coordinates(ship_ran):
                lst_check.append(j)
        print(gh.board_to_string(self.__board_size, [], {}, [], lst_check))
        while len(self.__ships) > 0:
            self.__play_one_round()
        gh.report_gameover()



############################################################
# An example usage of the game
############################################################
if __name__=="__main__":
    '''
    calls all the functions and basically runs the game
    '''
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()
