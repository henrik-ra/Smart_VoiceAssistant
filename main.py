# main.py
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

class CameraApp(App):
    def build(self):
        self.img1 = Image()
        
        # FloatLayout ermöglicht es uns, die Position und Größe der Schaltflächen flexibel zu gestalten
        layout = FloatLayout()
        
        # Kameraansicht
        self.img1.size_hint = (1, 1)
        layout.add_widget(self.img1)
        
        # Schaltflächen erstellen
        btn_prev_bg = Button(
            text='⮜', 
            size_hint=(None, None), 
            size=(50, 50),
            pos_hint={'x': 0.05, 'y': 0.1}, 
            background_normal='', 
            background_color=(1, 1, 1, 0.3)  # Transparent
        )
        btn_next_bg = Button(
            text='⮞', 
            size_hint=(None, None), 
            size=(50, 50),
            pos_hint={'x': 0.85, 'y': 0.1}, 
            background_normal='', 
            background_color=(1, 1, 1, 0.3)  # Transparent
        )
        btn_exit = Button(
            text='✕', 
            size_hint=(None, None), 
            size=(50, 50),
            pos_hint={'x': 0.9, 'y': 0.85}, 
            background_normal='', 
            background_color=(1, 0, 0, 0.3)  # Leicht transparentes Rot
        )
        
        # Schaltflächen binden
        btn_prev_bg.bind(on_press=self.prev_background)
        btn_next_bg.bind(on_press=self.next_background)
        btn_exit.bind(on_press=self.stop_app)
        
        # Schaltflächen zum Layout hinzufügen
        layout.add_widget(btn_prev_bg)
        layout.add_widget(btn_next_bg)
        layout.add_widget(btn_exit)

        self.capture = cv2.VideoCapture(0)  # Kamera initialisieren
        if not self.capture.isOpened():
            raise Exception("Kamera konnte nicht geöffnet werden")

        self.segmentor = SelfiSegmentation()  # CVZone Segmentor initialisieren
        self.load_background_images()
        self.indexImg = 0

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def load_background_images(self):
        background_images_path = './pics'
        if not os.path.exists(background_images_path):
            raise FileNotFoundError(f'Das Verzeichnis {background_images_path} existiert nicht')

        self.imgList = []
        listImg = os.listdir(background_images_path)
        for imgPath in listImg:
            img = cv2.imread(os.path.join(background_images_path, imgPath))
            img = cv2.resize(img, (640, 480))
            self.imgList.append(img)

    def update(self, dt):
        success, img = self.capture.read()
        if not success or img is None:
            print("Bild konnte nicht von der Kamera gelesen werden")
            return
        
        img = cv2.resize(img, (640, 480))
        imgOut = self.segmentor.removeBG(img, self.imgList[self.indexImg])
        
        buf1 = cv2.flip(imgOut, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(size=(imgOut.shape[1], imgOut.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img1.texture = image_texture

    def prev_background(self, instance):
        if self.indexImg > 0:
            self.indexImg -= 1

    def next_background(self, instance):
        if self.indexImg < len(self.imgList) - 1:
            self.indexImg += 1

    def stop_app(self, instance):
        self.capture.release()
        cv2.destroyAllWindows()
        App.get_running_app().stop()

if __name__ == '__main__':
    CameraApp().run()


# # main.py
# from kivy.app import App
# from kivy.uix.image import Image
# from kivy.clock import Clock
# from kivy.graphics.texture import Texture
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# import cv2
# from cvzone.SelfiSegmentationModule import SelfiSegmentation
# import os

# class CameraApp(App):
#     def build(self):
#         self.img1 = Image()
#         layout = BoxLayout(orientation='vertical')

#         # Navigation Buttons
#         btn_prev_bg = Button(text='Vorheriger Hintergrund')
#         btn_next_bg = Button(text='Nächster Hintergrund')
#         btn_exit = Button(text='Beenden')

#         btn_prev_bg.bind(on_press=self.prev_background)
#         btn_next_bg.bind(on_press=self.next_background)
#         btn_exit.bind(on_press=self.stop_app)

#         layout.add_widget(self.img1)
#         layout.add_widget(btn_prev_bg)
#         layout.add_widget(btn_next_bg)
#         layout.add_widget(btn_exit)

#         self.capture = cv2.VideoCapture(0)  # Kamera initialisieren
#         if not self.capture.isOpened():
#             raise Exception("Kamera konnte nicht geöffnet werden")

#         self.segmentor = SelfiSegmentation()  # CVZone Segmentor initialisieren
#         self.load_background_images()
#         self.indexImg = 0

#         Clock.schedule_interval(self.update, 1.0 / 30.0)
#         return layout

#     def load_background_images(self):
#         background_images_path = '../pics'
#         if not os.path.exists(background_images_path):
#             raise FileNotFoundError(f'Das Verzeichnis {background_images_path} existiert nicht')

#         self.imgList = []
#         listImg = os.listdir(background_images_path)
#         for imgPath in listImg:
#             img = cv2.imread(os.path.join(background_images_path, imgPath))
#             img = cv2.resize(img, (640, 480))
#             self.imgList.append(img)

#     def update(self, dt):
#         success, img = self.capture.read()
#         if not success or img is None:
#             print("Bild konnte nicht von der Kamera gelesen werden")
#             return
        
#         img = cv2.resize(img, (640, 480))
#         imgOut = self.segmentor.removeBG(img, self.imgList[self.indexImg])  # Threshold entfernt
        
#         buf1 = cv2.flip(imgOut, 0)
#         buf = buf1.tobytes()
#         image_texture = Texture.create(size=(imgOut.shape[1], imgOut.shape[0]), colorfmt='bgr')
#         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#         self.img1.texture = image_texture

#     def prev_background(self, instance):
#         if self.indexImg > 0:
#             self.indexImg -= 1

#     def next_background(self, instance):
#         if self.indexImg < len(self.imgList) - 1:
#             self.indexImg += 1

#     def stop_app(self, instance):
#         self.capture.release()
#         cv2.destroyAllWindows()
#         App.get_running_app().stop()

# if __name__ == '__main__':
#     CameraApp().run()




# # main.py
# from kivy.app import App
# from kivy.uix.image import Image
# from kivy.clock import Clock
# from kivy.graphics.texture import Texture
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# import cv2
# from cvzone.SelfiSegmentationModule import SelfiSegmentation
# import os

# class CameraApp(App):
#     def build(self):
#         self.img1 = Image()
#         layout = BoxLayout(orientation='vertical')

#         # Navigation Buttons
#         btn_prev_bg = Button(text='Vorheriger Hintergrund')
#         btn_next_bg = Button(text='Nächster Hintergrund')
#         btn_exit = Button(text='Beenden')

#         btn_prev_bg.bind(on_press=self.prev_background)
#         btn_next_bg.bind(on_press=self.next_background)
#         btn_exit.bind(on_press=self.stop_app)

#         layout.add_widget(self.img1)
#         layout.add_widget(btn_prev_bg)
#         layout.add_widget(btn_next_bg)
#         layout.add_widget(btn_exit)

#         self.capture = cv2.VideoCapture(0)  # Kamera initialisieren
#         if not self.capture.isOpened():
#             raise Exception("Kamera konnte nicht geöffnet werden")

#         self.segmentor = SelfiSegmentation()  # CVZone Segmentor initialisieren
#         self.load_background_images()
#         self.indexImg = 0

#         Clock.schedule_interval(self.update, 1.0 / 30.0)
#         return layout

#     def load_background_images(self):
#         background_images_path = '../pics'
#         if not os.path.exists(background_images_path):
#             raise FileNotFoundError(f'Das Verzeichnis {background_images_path} existiert nicht')

#         self.imgList = []
#         listImg = os.listdir(background_images_path)
#         for imgPath in listImg:
#             img = cv2.imread(os.path.join(background_images_path, imgPath))
#             img = cv2.resize(img, (640, 480))
#             self.imgList.append(img)

#     def update(self, dt):
#         success, img = self.capture.read()
#         if not success or img is None:
#             print("Bild konnte nicht von der Kamera gelesen werden")
#             return
        
#         img = cv2.resize(img, (640, 480))
#         imgOut = self.segmentor.removeBG(img, self.imgList[self.indexImg], threshold=0.8)
        
#         buf1 = cv2.flip(imgOut, 0)
#         buf = buf1.tobytes()
#         image_texture = Texture.create(size=(imgOut.shape[1], imgOut.shape[0]), colorfmt='bgr')
#         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#         self.img1.texture = image_texture

#     def prev_background(self, instance):
#         if self.indexImg > 0:
#             self.indexImg -= 1

#     def next_background(self, instance):
#         if self.indexImg < len(self.imgList) - 1:
#             self.indexImg += 1

#     def stop_app(self, instance):
#         self.capture.release()
#         cv2.destroyAllWindows()
#         App.get_running_app().stop()

# if __name__ == '__main__':
#     CameraApp().run()