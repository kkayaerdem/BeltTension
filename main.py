from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

# Katalog ve hesaplama fonksiyonları
CATALOG = {
    "AT5": {
        "mkg": 0.0033,
        "widths": {10: 516.0, 16: 826.0, 25: 1290.0, 32: 1651.0, 50: 2580.0, 75: 3870.0, 100: 5160.0}
    },
    "ATL5": {
        "mkg": 0.0028,
        "widths": {10: 516.0, 16: 826.0, 25: 1290.0, 32: 1651.0, 50: 2580.0, 75: 3870.0, 100: 5160.0, 150: 7740.0}
    },
    "AT10": {
        "mkg": 0.0057,
        "widths": {16: 1651.0, 25: 2580.0, 32: 3302.0, 50: 5160.0, 75: 7740.0, 100: 10320.0, 150: 15480.0}
    },
    "ATL10": {
        "mkg": 0.0067,
        "widths": {16: 1651.0, 25: 2580.0, 32: 3302.0, 50: 5160.0, 75: 7740.0, 100: 10320.0, 150: 15480.0}
    },
    "AT20": {
        "mkg": 0.0097,
        "widths": {25: 5430.0, 32: 6950.0, 50: 10860.0, 75: 16290.0, 100: 21720.0, 150: 32580.0}
    },
    "ATL20": {
        "mkg": 0.0107,
        "widths": {32: 6950.0, 50: 10860.0, 75: 16290.0, 100: 21720.0, 150: 32580.0}
    }
}

def calculate_F(mkg, width_mm, L_m, f_hz):
    kayisEn_m = width_mm / 1000.0
    return 4.0 * (mkg * kayisEn_m) * (L_m ** 2) * (f_hz ** 2)

def adjust_normalF(normalF, role):
    return normalF * (23.0/80.0) if role == "Avare" else normalF * 0.5

def evaluate(F, normalF):
    if F > normalF:
        return "Fazla Gergin"
    elif F < 0.8 * normalF:
        return "Gevşek"
    else:
        return "Uygun (±%20 aralığında)"

class BeltCalcApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        scroll = ScrollView()
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Başlık
        title = Label(text='[b]Kayış Gergi Hesabı[/b]', size_hint_y=None, height=40, markup=True, font_size='18sp')
        content.add_widget(title)
        
        # Kayış türü
        content.add_widget(Label(text='[b]Kayış Türü:[/b]', size_hint_y=None, height=30, markup=True))
        self.belt_spinner = Spinner(
            text='AT5',
            values=tuple(sorted(CATALOG.keys())),
            size_hint_y=None,
            height=44
        )
        self.belt_spinner.bind(text=self.on_belt_change)
        content.add_widget(self.belt_spinner)
        
        # Kayış eni
        content.add_widget(Label(text='[b]Kayış Eni (mm):[/b]', size_hint_y=None, height=30, markup=True))
        self.width_spinner = Spinner(
            text='10',
            values=('10', '16', '25', '32', '50', '75', '100', '150'),
            size_hint_y=None,
            height=44
        )
        content.add_widget(self.width_spinner)
        
        # Serbest salınım boyu
        content.add_widget(Label(text='[b]Serbest Salınım Boyu L:[/b]', size_hint_y=None, height=30, markup=True))
        length_layout = BoxLayout(size_hint_y=None, height=44, spacing=10)
        self.L_input = TextInput(text='1', multiline=False, input_filter='float', size_hint_x=0.7)
        self.L_unit_spinner = Spinner(
            text='m',
            values=('m', 'cm', 'mm'),
            size_hint_x=0.3
        )
        length_layout.add_widget(self.L_input)
        length_layout.add_widget(self.L_unit_spinner)
        content.add_widget(length_layout)
        
        # Frekans
        content.add_widget(Label(text='[b]Frekans f (Hz):[/b]', size_hint_y=None, height=30, markup=True))
        self.freq_input = TextInput(text='10', multiline=False, input_filter='float')
        content.add_widget(self.freq_input)
        
        # Rol
        content.add_widget(Label(text='[b]Rol:[/b]', size_hint_y=None, height=30, markup=True))
        self.role_spinner = Spinner(
            text='Avare',
            values=('Avare', 'Tahrik'),
            size_hint_y=None,
            height=44
        )
        content.add_widget(self.role_spinner)
        
        # Hesapla butonu
        calc_btn = Button(text='HESAPLA', size_hint_y=None, height=50, background_color=(0.2, 0.6, 0.8, 1))
        calc_btn.bind(on_press=self.on_calculate)
        content.add_widget(calc_btn)
        
        # Sonuç etiketi
        self.result_label = Label(text='Sonuç burada görünecek', size_hint_y=None, height=250, markup=True)
        content.add_widget(self.result_label)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def on_belt_change(self, spinner, text):
        # Seçilen kayışa uygun enler güncelle
        widths = sorted(CATALOG[text]['widths'].keys())
        self.width_spinner.values = tuple(str(w) for w in widths)
        self.width_spinner.text = str(widths[0])
    
    def on_calculate(self, instance):
        try:
            # Girdileri al
            belt_name = self.belt_spinner.text
            width_mm = int(self.width_spinner.text)
            L_val = float(self.L_input.text)
            L_unit = self.L_unit_spinner.text
            freq = float(self.freq_input.text)
            role = self.role_spinner.text
            
            # L'yi metreye çevir
            if L_unit == 'mm':
                L_m = L_val / 1000.0
            elif L_unit == 'cm':
                L_m = L_val / 100.0
            else:
                L_m = L_val
            
            # Katalogdan mkg ve normalF al
            belt = CATALOG[belt_name]
            mkg = belt['mkg']
            normalF_base = belt['widths'][width_mm]
            
            # Hesapla
            F = calculate_F(mkg, width_mm, L_m, freq)
            normalF_adj = adjust_normalF(normalF_base, role)
            status = evaluate(F, normalF_adj)
            diff_pct = (F - normalF_adj) / normalF_adj * 100 if normalF_adj else 0
            
            # Sonuç göster
            result_text = f"""[b]SONUÇLAR[/b]
Kayış: {belt_name}
Kayış Eni: {width_mm} mm
Rol: {role}
Serbest Salınım Boyu: {L_m:.3f} m
Frekans: {freq:.3f} Hz

[b]Hesaplanan F:[/b] {F:.3f} N
[b]Referans normalF:[/b] {normalF_adj:.3f} N
[b]F Farkı:[/b] {diff_pct:+.1f}%

[color=00ff00][b]Durum: {status}[/b][/color]
            """
            self.result_label.text = result_text
        except ValueError as ve:
            self.result_label.text = f'[color=ff0000][b]Hata:[/b] Lütfen geçerli sayı girin[/color]'
        except Exception as e:
            self.result_label.text = f'[color=ff0000][b]Hata:[/b] {str(e)}[/color]'

if __name__ == '__main__':
    BeltCalcApp().run()
