package com.novibe.common.base_structures;

import com.google.gson.Gson;
import com.novibe.App;

public interface Jsonable {

    Gson mapper = App.commonContext.getBean(Gson.class);

    default String toJson() {
        return mapper.toJson(this);
    }

}
