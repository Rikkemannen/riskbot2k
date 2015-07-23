__author__ = 'rickard'
import unittest
from mock import patch
from controller.game_actions import war, battle, throw_die
from model.world import Territory
from view.blobapp import Blob
from controller.setup_board import Player
from controller.game_actions import conquer_territory

class CombatTestCase(unittest.TestCase):

    def test_die_high(self):
        res = throw_die(200)
        self.assertLessEqual(max(res),6)

    def test_die_low(self):
        res = throw_die(200)
        self.assertGreater(min(res),0)

    @patch('controller.game_actions.throw_die')
    def test_battle(self,mock_method):
        p1 = Territory('',None,2)
        p2 = Territory('',None,1)
        mock_method.side_effect = [[6],[6]]
        res = battle(p1,p2, 1)
        self.assertTrue(res)

    @patch('controller.game_actions.throw_die')
    def test_war_jonas_vinner(self,mock_method):
        p1 = Territory('',None,2)
        p2 = Territory('',None,1)
        mock_method.side_effect = [[6],[6]]
        res = war(p1,p2, 1)
        self.assertEqual(res, p2)

    @patch('controller.game_actions.throw_die')
    def test_war_rickard_vinner(self,mock_method):
        p1 = Territory('',None,2)
        p2 = Territory('',None,1)
        mock_method.side_effect = [[6],[5]]
        res = war(p1,p2, 1)
        self.assertEqual(res, p1)

    @patch('controller.game_actions.throw_die')
    def test_war_flera_dies_jonas_win(self,mock_method):
        p1 = Territory('',None,2)
        p2 = Territory('',None,2)
        mock_method.side_effect = [[6],[5,6]]
        res = war(p1,p2, 1)
        self.assertEqual(res, p2)

    @patch('controller.game_actions.throw_die')
    def test_war_flera_dies_rickard_win(self,mock_method):
        p1 = Territory('',None,2)
        p2 = Territory('',None,1)
        mock_method.side_effect = [[5,6],[5]]
        res = war(p1,p2, 1)
        self.assertEqual(res, p1)

    #TODO fixa config-problemet! IOError: Reading configspec failed: Config file not found: "..\conf\board_spec.ini".
    def test_conquer_territory(self):
        t1 = Territory('',None,3)
        t2 = Territory('',None,0)
        p1 = Player('rickard',None)
        p2 = Player('jonas', None)
        winner = Blob(0,0,t1)
        looser = Blob(0,0,t2)
        winner.set_owner(p1)
        looser.set_owner(p2)
        conquer_territory(winner,looser, 2)
        self.assertEqual(winner.get_soldiers(),1)
if __name__ == '__main__':
    unittest.main()