import cv2

OVERLAY_BACKGROUND = cv2.imread('textures/overlay.png')
def create_overlay(time, score):
    screen = cv2.imread('textures/overlay.png')
    screen = cv2.putText(screen, f'TIME: {time:05.1f}', (10,40), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
    screen = cv2.putText(screen, f'SCORE: {score:02d}', (10,80), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
    return screen

def victory_screen(time):
    screen = cv2.imread('textures/victory.png')
    screen = cv2.putText(screen, f'Victory! Time: {time:.2f}s', (10,150), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,255,255), 4)
    return screen
if __name__ == '__main__':
    #screen = create_overlay(20.2344, 20)
    #print(f'TIME: {20.2344:05.1f}')
    screen = victory_screen(20.25)
    cv2.imshow('window', screen)
    cv2.waitKey(0)
    