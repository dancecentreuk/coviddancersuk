gender_choices = [
    ('M', 'MALE'),
    ('F', 'FEMALE')
]


location_choices = [
    ('Brighton', 'Brighton'),
    ('Leeds', 'Leeds'),
    ('Liverpool', 'Liverpool'),
    ('Manchester', 'Manchester')
]

dance_styles = [
    ('Ballet', 'Ballet'),
    ('Jazz', 'Jazz'),
    ('Tap', 'Tap')
]

work_choices = [
    ('True', 'Postings'),
    ('False', 'Jobs')
]

hours = ([(str(x), str(x)) for x in range(1, 25)])

height_ft = ([(str(x), str(x)) for x in range(1, 9)])

height_in = ([(str(x), str(x)) for x in range(1, 12)])

weight_st = ([(str(x), str(x)) for x in range(1, 20)])

weight_lb = ([(str(x), str(x)) for x in range(1, 14)])

waist = ([(str(x), str(x)) for x in range(21, 48)])

bust = ([(str(x), str(x)) for x in range(21, 54)])

hip = ([(str(x), str(x)) for x in range(21, 57)])

shoe_size = ([(str(x), str(x)) for x in range(1, 16)])

eye_color = [
    ('black', 'black'),
    ('blue', 'blue'),
    ('brown', 'brown'),
    ('hazel', 'hazel'),
    ('grey', 'grey'),
    ('green', 'green')
]

hair_color = [
    ('black', 'black'),
    ('brown', 'brown'),
    ('blonde', 'blonde'),
    ('red', 'red'),
    ('grey', 'grey'),
    ('white', 'white'),
    ('strawberry blonde', 'strawberry blonde'),

]

build = [
    ('slim', 'slim'),
    ('medium', 'medium'),
    ('muscular', 'muscular'),
    ('large', 'large'),
    ('very large', 'very large')
]

primary_job = [
    ('no option', 'no option'),
    ('choreographer', 'choreographer'),
    ('dance teacher', 'dance teacher'),
    ('dancer', 'dancer')
]