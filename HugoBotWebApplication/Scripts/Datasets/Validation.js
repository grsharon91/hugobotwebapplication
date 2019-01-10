

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
            Description: {
                required: true
            }

        },
        // Specify validation error messages
        messages: {
            Description: { required: "Please provide a description for your dataset" },
            DatasetName: { required: "Please specify a name for the dataset" },
            Category: { required: "Please choose a category" },
            Visiblity: { required: "Please choose visibliy for your dataset" },
            Path: { required: "Please choose a dataset file to upload" },
            VMap_file: { required: "Please choose a variable map file to upload" }
        },
        errorPlacement: function (error, element) {

            if (element.attr("name") == "VMap_file") {
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

