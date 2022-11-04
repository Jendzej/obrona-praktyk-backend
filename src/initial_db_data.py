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
        model_school_classes(school_class="1TE"),
        model_school_classes(school_class="1TET"),
        model_roles(role="admin"),
        model_roles(role="user"),
        model_payment_status(status="paid"),
        model_payment_status(status="not paid"),
        model_payment_status(status="pending"),
        model_payment_status(status="other")
    ])
