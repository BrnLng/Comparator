from Database import Database


class Singleton:
    """ used to be 'Borg' ~= a Singleton for Data.
     See Comparator and http://code.activestate.com/recipes/66531-singleton-we-dont-need-no-stinkin-singleton-the-bo/
     using Oren's Singleton """

    def __new__(type, *args, **kwargs):  # needed to add args & kwargs to pass database call later wtf
        if '_the_instance' not in type.__dict__:
            type._the_instance = object.__new__(type)
        # print('args', args)
        # print('kwargs', kwargs)
        return type._the_instance

    @staticmethod
    def database(new_list=None, partial_ordered_list=None):
        return Database(new_list, partial_ordered_list)
