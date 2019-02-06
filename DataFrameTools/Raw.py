class raw_data_df(pd.DataFrame):
    """
	Pass a "raw" dataset for first line cleaning/preperation.
    """

    def __init__(self, df, keep_subset_of_columns):
        super().__init__(df)  # initialize subclass from DataFrame instance
        
        self.raw_columns_not_kept = set(self.columns).difference(set(keep_subset_of_columns))
        
    def strip_white_space_from_dtype_object_columns(self):
        column_names = self.select_dtypes([object])\
                        .columns
        for i in column_names:
            self[i] = self[i].str.strip()
        return self