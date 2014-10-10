Resource -> ttl:300
    Rule simple_rule1 -> comment:"Example rule"
        SetCache -> aggressive:true

        Compose default_buffer ->
            Literal -> value:"<html><head><title>Example output</title></head><body><h1>Example output</h1></body>"
            Debug -> message:"we are debugging"
