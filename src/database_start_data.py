from src.data_functions import add_multiple_data


def initial_insertion(engine, initial_models):
    model_school_classes = initial_models[0]
    model_roles = initial_models[1]
    model_payment_status = initial_models[2]

    add_multiple_data(engine, [
        model_school_classes(school_class="1TIP"),
        model_school_classes(school_class="1TI1"),
        model_school_classes(school_class="1TI2"),
        model_school_classes(school_class="1TR"),
        model_school_classes(school_class="1TET"),
        model_school_classes(school_class="2TI1"),
        model_school_classes(school_class="2TI2"),
        model_school_classes(school_class="2TR"),
        model_school_classes(school_class="2TET"),
        model_school_classes(school_class="3TI1"),
        model_school_classes(school_class="3TI2"),
        model_school_classes(school_class="3TR"),
        model_school_classes(school_class="3TET"),
        model_school_classes(school_class="4TIP"),
        model_school_classes(school_class="4TI1"),
        model_school_classes(school_class="4TI2"),
        model_school_classes(school_class="4TR"),
        model_school_classes(school_class="4TOR"),
        model_school_classes(school_class="4TET"),
        model_school_classes(school_class="4TEP"),

        model_roles(role="admin"),
        model_roles(role="user"),

        model_payment_status(status="paid"),
        model_payment_status(status="not paid"),
        model_payment_status(status="pending"),
        model_payment_status(status="other")
    ])
