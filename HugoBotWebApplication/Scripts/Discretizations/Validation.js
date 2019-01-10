    // Wait for the DOM to be ready
    $(function () {
        // Initialize form validation on the registration form.
        // It has the name attribute "registration"
        $('#UploadDatasetForm').validate({
            errorElement: 'span',
            errorClass: "text-danger field-validation-error",
            // Specify validation rules
            rules: {
                // The key name on the left side is the name attribute
                // of an input field. Validation rules are defined
                // on the right side
                firstname: "required",
                lastname: "required",
                email: {
                    required: true,
                    // Specify that email should be validated
                    // by the built-in "email" rule
                    email: true
                },
                BinsNumber: {
                    required: true,
                    digits: true,
                    number: true,
                    min: 2
                },
                MaxGap: {
                    //required: true,
                    digits: true,
                    number: true
                },
                DatasetName: {
                    required: true
                },
                Category: {
                    required: true
                },

                Visiblity: {
                    required: true
                },
                Path: {
                    required: true
                },
                VMap_file: {
                    required: true
                },
                abstraction_method: {
                    required: true,
                    minlength: 1
                },
                td4c_param: {
                    required: "#td4c:checked",
                    minlength: 1
                },
                Description: {
                    required: true
                }
            },
            // Specify validation error messages
            messages: {
                firstname: "Please enter your firstname",
                BinsNumber: { required: "Please enter the bins number", digits: "Must be an integer greater than 1", number: "Must be an integer greater than 1" },
                MaxGap: { digits: "Must be an integer ", number: "Must be an integer " },
                DatasetName: { required: "Please specify a name for the dataset" },
                Category: { required: "Please choose a category" },
                Visiblity: { required: "Please choose visibliy for your dataset" },
                Path: { required: "Please choose a dataset file to upload" },
                VMap_file: { required: "Please choose a variable map file to upload" },
                td4c_param: "Please select at least one scoring method",
                abstraction_method: "Please select at least one abstraction method",
                Description: { required: "Please provide a description for your dataset" }


            },
            errorPlacement: function (error, element) {
                if (element.attr("name") == "td4c_param") {
                    error.insertAfter(".td4c_error");
                }

                else if (element.attr("name") == "abstraction_method") {
                    error.insertAfter("#showAbstractionMethodsButton");
                }
                else if (element.attr("name") == "VMap_file") {
                    error.insertAfter("#VMap_file_error")
                }
                else if (element.attr("name") == "Path") {
                    error.insertAfter("#Dataset_file_error")
                }
                else
                    error.insertAfter(element);
            },
            // Make sure the form is submitted to the destination defined
            // in the "action" attribute of the form when valid
            submitHandler: function (form) {
                form.submit();
            }
        });
    });

