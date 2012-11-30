

service Infer {
    list <double> infer(1:list <double> input)
    bool update_nnmachine(1:i64 nn_id)
    oneway void halt()
}
