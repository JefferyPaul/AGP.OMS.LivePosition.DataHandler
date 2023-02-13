"""

"""

import os
import sys
from time import sleep
from datetime import datetime, date, time
import threading
import argparse
import subprocess


PATH_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PATH_ROOT)

from helper.scheduler import ScheduleRunner
from helper.simpleLogger import MyLogger


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--interval', default=60)
args = arg_parser.parse_args()
INTERVAL = int(args.interval)


class MyScheduler(ScheduleRunner):
    def __init__(
            self,
            running_time: list,  # ScheduleRunner
            interval=300,
            logger=MyLogger('RtdMonitor'),
    ):
        # 定时任务骑
        super(MyScheduler, self).__init__(running_time=running_time, logger=logger, schedule_checking_interval=interval)
        self._task_interval = interval
        self._task_processing_thread: None or threading.Thread = None

    def _start_task(self):
        self._task_processing_thread = threading.Thread(target=self._task_processing_loop)
        self._task_processing_thread.start()

    def _end_task(self):
        self.logger.info('正在等待线程结束...')
        if self._task_processing_thread:
            self._task_processing_thread.join()
        self.logger.info('线程已终止!')

    def _task_processing_loop(self):
        p_1_get_position_bat = os.path.join(PATH_ROOT, '_1.GetTraderPosition.bat')
        p_2_get_initx = os.path.join(PATH_ROOT, '_2.GetTraderInitX.bat')
        p_3_cal = os.path.join(PATH_ROOT, '_3.GenPerInitXPosition.AIO.bat')
        p_4_cal = os.path.join(PATH_ROOT, '_3.GenPerInitXPosition.Selected.bat')

        l_bat = [p_1_get_position_bat, p_2_get_initx, p_3_cal, p_4_cal]

        while self.schedule_in_running:
            # _error = False
            for _bat in l_bat:
                self.logger.info(f'calling {_bat}')
                # os.popen(f'call {_bat}')
                try:
                    subprocess.run(
                        f'call {_bat}',
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        encoding="utf-8", timeout=60
                    )
                except Exception as e:
                    print(e)
                    # _error = True
                    self.logger.warning('call bat error')
                    break                
            print('\n')
            sleep(self._task_interval)


if __name__ == '__main__':
    my_logger = MyLogger('rtd bat scheduler')

    # 运行bat 更新数据 =========================
    bat_scheduler = MyScheduler(
        running_time=[
            [time(9, 0, 0), time(11, 32, 0)],
            [time(13, 30, 0), time(15, 2, 0)],
            [time(21, 0, 0), time(23, 2, 0)],
        ],
        interval=INTERVAL,
        logger=my_logger
    )
    bat_scheduler.start()
