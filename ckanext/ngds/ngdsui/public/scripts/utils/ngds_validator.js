/**
 * @author - Vivek
 * This is a bunch of awesomeness. This function validates HTML form fields dynamically and is purely based on information that is put into the HTML itself
 * in 'data-' custom tags. The following attributes on an input element are needed -
 *
 * data-validate - A marker attribute with no value. It indicates to the validator function that it should be validated.
 * data-validate-fingerprint - An attribute that indicates to the function what it means for this field to be valid, as well as invalid.
 *                              It's value looks something like this - "2^^^100^^^[a-zA-Z1-9\-]^^^2". Three ^^^ characters are used as separators between values.
 *
 *                              The first value indicates the minimum length that the value of this input can be in order to be valid.
 *
 *                              The second value indicates the maximum length that the value of this input can be in order to be valid.
 *
 *                              The third value indicates the characters that are allowed in this input's value for it to be valid (More importantly, the characters that
 *                              render it invalid, which is inferred by the validator function and lets the programmer focus on what the valid inputs are.)
 *
 *                             The fourth value indicates after how many characters are entered into the input field, to begin validating the input. This reduces the signal/noise ratio
 *                             for the user by not telling them that an input is invalid before they have even attempted to enter a fully considered input.
 *
 * data-validate-regex-msg - Let the user know that they have entered invalid characters using a message typed into this attribute's value.
 * data-validate-minlen-msg - Let the user know that they have entered too few characters using a message typed into this attribute's value.
 * data-validate-maxlen-msg - Let the user know that they have entered too many characters using a message typed into this attribute's value.
 *
 *
 */

ngds.validator = (function () {

    var _validator = function () {
        var me = this;

        this.setup_fields = function () {
            var fields_to_validate = $("[data-validate]").filter("[data-validate-fingerprint]");

            $(fields_to_validate).each(function () {

                var rules = $(this).attr('data-validate-fingerprint').split("^^^");

                var validation_begin_bound = 0;
                var invalidation_fng = null;

                if (typeof rules[2] !== "undefined") {
                    var ind = rules[2].indexOf("[");
                    var regex_validate;
                    if (ind === -1) {
                        regex_validate = function (val) {
                            invalidation_fng = new RegExp(rules[2]);
                            for (var i = 0; i < val.length; i++) {
                                if (val[i].match(invalidation_fng) === null) {
                                    return false;
                                }
                            }
                            return true;
                        }
                    }
                    else {
                        var inter_arr = rules[2].split("");
                        inter_arr.splice(ind + 1, 0, "^");
                        invalidation_fng = new RegExp(inter_arr.join(""));
                        regex_validate = function (val) {
                            if (invalidation_fng.exec(val) !==
                                null) {
                                return false;
                            }
                            return true;
                        }
                    }
                }

                var maxlength_rule = Number(rules[1]);
                var minlength_rule = Number(rules[0]);

                if (typeof rules[3] !== "undefined") {
                    validation_begin_bound = Number(rules[3]);
                }

                console.log(maxlength_rule, minlength_rule);
                var keystrokes = 0;
                $(this).on('input', function () {
                        keystrokes = keystrokes + 1;
                        var cur_val = $(this).val();

                        if (keystrokes >= validation_begin_bound) {
                            $(this).parents().children().filter(".error-block").remove();
                            if (regex_validate(cur_val) === false) {
                                $(this).after($("<div/>", {"class": "error-block", "text": $(this).attr("data-validate-regex-msg")}));
                            }
                            if (cur_val.length > maxlength_rule) {
                                $(this).after($("<div/>", {"class": "error-block", "text": $(this).attr("data-validate-maxlen-msg")}));
                            }
                            if (cur_val.length < minlength_rule) {
                                $(this).after($("<div/>", {"class": "error-block", "text": $(this).attr("data-validate-minlen-msg")}));
                            }
                        }

                    }
                );
            });

        };

        this.initialize = function () {
            me.setup_fields();
        }

        return {
            'initialize': this.initialize
        };

    };

    var validator_instance = null;

    var initialize = function () {
        if (validator_instance === null) {
            validator_instance = new _validator();
            validator_instance.initialize();
        }
    };

    return {
        'initialize': initialize
    }

})
    ();

$(document).ready(function () {
    ngds.validator.initialize();
});